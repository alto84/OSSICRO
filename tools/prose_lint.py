"""Prose drift detector for the OSSICRO cleanup pass.

Implements the detection spec from docs/writing/language-drift-analysis.md
(sections 5.2, 5.3, 5.6). It measures the density of the drift constructions
rather than banning phrases, because the project's own phrase blacklist was
routed around by a newer dialect. The point of the tool is to let the cleanup
prove it lowered the numbers instead of trading one house style for another.

Usage:
    python tools/prose_lint.py <file-or-glob> [<file-or-glob> ...]

Reports per-file metrics and a corpus total, and marks each metric PASS/OVER
against the targets for user-facing and outward text. Fenced code blocks and
markdown table rows are excluded from prose counts.
"""

from __future__ import annotations

import glob
import re
import sys
from collections import defaultdict

# Targets from the report's baseline table (section 5.6), for user-facing and
# outward text. Internal working notes are held to no target here.
TARGETS = {
    "em_dashes_per_1k": 5.0,
    "contrastive_per_1k": 1.5,
    "honest_family_per_1k": 0.3,   # "about 0 outside genuine ethics content"
    "arrows_in_prose": 0,
    "tier1_lexicon_hits": 0,
}

# Grade-3 register vocabulary (the drift proper). Terms of art that survive a
# cleanup (fail-closed, verbatim-locked) are deliberately NOT here.
TIER1_LEXICON = [
    r"\bload-bearing\b", r"\bkeystone\b", r"\bmarquee\b", r"\bmoat\b",
    r"\btrust wedge\b", r"\bhard rail\b", r"\blong pole\b", r"\bposture\b",
    r"\bsubstrate\b", r"\bspine\b", r"\bby construction\b",
    r"\b(?:true|holds) by absence\b", r"\w+-shaped\b", r"\bthe hard line\b",
]
_TIER1 = [re.compile(p, re.IGNORECASE) for p in TIER1_LEXICON]

_HONEST = re.compile(r"\b(?:honest|honestly|honesty|dishonest|dishonestly)\b", re.I)
_CONTRASTIVE = re.compile(r",\s+(?:not|never)\s", re.I)
_ARROW = re.compile(r"→|->")
_APHORISM = re.compile(
    r"\bis (?:the point|itself the|the entire|the (?:whole )?"
    r"(?:theory|protection|gate|substrate|spine|wedge|moat|thesis))\b", re.I)
_MIDCAPS = re.compile(r"(?<![>#`])\b([A-Z]{3,})\b")
_ACRONYMS = {
    "CFR", "FDA", "IRB", "LOA", "IND", "DMF", "PHI", "SAE", "ADE", "HIPAA",
    "SNOMED", "LOINC", "RXNORM", "ICD", "FHIR", "SMART", "UI", "URL", "PDF",
    "FDF", "API", "HTTP", "JSON", "SHA", "UUID", "HTML", "CSS", "MVP", "CRO",
    "DSMB", "NCT", "RWE", "CDS", "OSSICRO", "TODO", "DRAFT", "NFC", "HMAC",
    "GAP", "INV", "HC", "OPM", "DPAPI", "NCBI", "FDCA", "US", "USC", "EA",
    "AND", "OR", "NOT", "GET", "POST", "NEVER", "ONLY", "READ",
}


def _strip_noise(text: str) -> str:
    """Remove fenced code blocks and markdown table rows from prose counting."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.lstrip().startswith("|"):        # markdown table row
            continue
        out.append(line)
    return "\n".join(out)


def _sentences(text: str):
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = s.strip()
        if s:
            yield s


def analyze(path: str) -> dict:
    raw = open(path, encoding="utf-8", errors="replace").read()
    text = _strip_noise(raw)
    words = len(re.findall(r"\b\w+\b", text)) or 1
    k = words / 1000.0
    midcaps = [m.group(1) for m in _MIDCAPS.finditer(text)
               if m.group(1) not in _ACRONYMS]
    short_sentences = [s for s in _sentences(text) if len(s.split()) <= 12]
    return {
        "path": path,
        "words": words,
        "em_dashes_per_1k": text.count("—") / k,
        "contrastive_per_1k": len(_CONTRASTIVE.findall(text)) / k,
        "honest_family_per_1k": len(_HONEST.findall(text)) / k,
        "arrows_in_prose": len(_ARROW.findall(text)),
        "tier1_lexicon_hits": sum(len(rx.findall(text)) for rx in _TIER1),
        "aphorisms": len(_APHORISM.findall(text)),
        "midcaps": len(midcaps),
        "_short_sentences": short_sentences,
    }


def main(patterns):
    paths = []
    for p in patterns:
        paths.extend(sorted(glob.glob(p, recursive=True)))
    paths = [p for p in paths if p.lower().endswith((".md", ".html", ".txt"))]
    if not paths:
        print("no .md/.html/.txt files matched", file=sys.stderr)
        return 2

    reports = [analyze(p) for p in paths]

    # Maxim echo: short sentences appearing verbatim in two or more files.
    seen = defaultdict(set)
    for r in reports:
        for s in set(r["_short_sentences"]):
            norm = re.sub(r"\s+", " ", s.lower()).strip(" .")
            if len(norm) > 20:
                seen[norm].add(r["path"])
    echoes = {s: sorted(f) for s, f in seen.items() if len(f) > 1}

    hdr = ("%-46s %7s %6s %6s %6s %5s %5s" %
           ("file", "words", "em/1k", "not/1k", "hon/1k", "arrw", "lex"))
    print(hdr)
    print("-" * len(hdr))
    tot = defaultdict(float)
    for r in sorted(reports, key=lambda x: -x["em_dashes_per_1k"]):
        name = r["path"].replace("\\", "/")
        name = name[-45:] if len(name) > 45 else name
        flag = lambda key: "!" if r[key] > TARGETS[key] else " "
        print("%-46s %7d %5.1f%s %5.1f%s %5.1f%s %4d%s %4d%s" % (
            name, r["words"],
            r["em_dashes_per_1k"], flag("em_dashes_per_1k"),
            r["contrastive_per_1k"], flag("contrastive_per_1k"),
            r["honest_family_per_1k"], flag("honest_family_per_1k"),
            r["arrows_in_prose"], flag("arrows_in_prose"),
            r["tier1_lexicon_hits"], flag("tier1_lexicon_hits")))
        for key in ("words", "em_raw", "contrastive_raw", "honest_raw",
                    "arrows_in_prose", "tier1_lexicon_hits", "aphorisms", "midcaps"):
            pass
        tot["words"] += r["words"]
        tot["em"] += r["em_dashes_per_1k"] * r["words"] / 1000.0
        tot["contrastive"] += r["contrastive_per_1k"] * r["words"] / 1000.0
        tot["honest"] += r["honest_family_per_1k"] * r["words"] / 1000.0
        tot["arrows"] += r["arrows_in_prose"]
        tot["lex"] += r["tier1_lexicon_hits"]
        tot["aphorisms"] += r["aphorisms"]
        tot["midcaps"] += r["midcaps"]

    kk = tot["words"] / 1000.0 or 1
    print("-" * len(hdr))
    print("CORPUS: %d words | em/1k %.1f (target <=%.1f) | not-never/1k %.1f (<=%.1f) "
          "| honest/1k %.1f (<=%.1f) | arrows %d (0) | lexicon %d (0) | aphorisms %d | midcaps %d"
          % (tot["words"], tot["em"] / kk, TARGETS["em_dashes_per_1k"],
             tot["contrastive"] / kk, TARGETS["contrastive_per_1k"],
             tot["honest"] / kk, TARGETS["honest_family_per_1k"],
             int(tot["arrows"]), int(tot["lex"]), int(tot["aphorisms"]),
             int(tot["midcaps"])))
    print("maxim echoes (same short sentence in >=2 files): %d" % len(echoes))
    for s, files in list(echoes.items())[:8]:
        print("   \"%s...\"  in %s" % (s[:60], ", ".join(f.split("/")[-1] for f in files)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["docs/**/*.md"]))
