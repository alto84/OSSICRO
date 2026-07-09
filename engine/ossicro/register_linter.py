"""REGISTER TRIPWIRE: fast, fallible, and non-authoritative for voice.

A zero-LLM regex pass that catches known LLM mannerisms in milliseconds. It is
deliberately subordinate: it certifies the absence of listed strings, not the
presence of professional register, so a clean lint is not a voice claim. Voice
authority belongs to the concept-based reviewer applying
docs/WRITING-PRINCIPLES.md, whose findings fail toward the human gate and
whose judgment improves with every model generation; this list improves only
by hand.

Two rule classes here are genuine hard rules with deterministic hard-fail
authority, because they are fact-shaped and never become legitimate:
chat-transcript residue (AI self-reference, chatbot openers) and the
21 CFR 50.20 exculpatory-consent constructions. Everything else in the
registry is a dated, non-blocking smoke signal whose patterns double as
illustrative examples seeding the voice reviewer's rubric. Expect the example
tier to decay as models and writing norms change; retire entries freely -- the
principles, not the patterns, are the standard (docs/VALIDATION-PHILOSOPHY.md).

A finding is a flag for human review or an automated rewrite pass, never a
silent edit. The engine never changes a human-vetted verbatim passage.

Tiering: a finding's EFFECTIVE tier is 'hard-rule' only for an unscoped
hard-rule, or for a scoped hard-rule (e.g. 21 CFR 50.20, scope='consent') when
the linted document's category matches the scope. A scoped hard rule seen with
an unknown document category is downgraded to 'example' (advisory, surfaced but
non-blocking) so it cannot false-fail outside its context. Only a hard-rule
finding can make a document fail; example findings never gate a release.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

ENGINE_ROOT = Path(__file__).resolve().parent.parent
_REGISTRY_PATH = ENGINE_ROOT / "registry" / "banned-constructions.json"

_SEVERITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}


@dataclass
class LintFinding:
    rule_id: str
    category: str
    severity: str
    tier: str          # effective tier: 'hard-rule' (gating) or 'example' (advisory)
    line: int
    col: int
    match_text: str
    message: str
    suggestion: str
    citation: str = ""


@dataclass
class LintReport:
    findings: List[LintFinding] = field(default_factory=list)
    words: int = 0

    @property
    def hard_findings(self) -> List[LintFinding]:
        return [f for f in self.findings if f.tier == "hard-rule"]

    @property
    def example_findings(self) -> List[LintFinding]:
        return [f for f in self.findings if f.tier == "example"]

    @property
    def example_density_per_1k(self) -> float:
        """Informational only: weighted example-tier signal per 1k words. NOT a gate."""
        score = sum(_SEVERITY_WEIGHT.get(f.severity, 1) for f in self.example_findings)
        return round(1000.0 * score / self.words, 2) if self.words else 0.0

    def passes(self) -> bool:
        """A document passes the tripwire iff it has NO hard-rule finding.
        Example-tier findings never gate a release -- they are a non-blocking
        smoke signal; voice authority is the concept-based reviewer."""
        return not self.hard_findings

    def by_category(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for f in self.findings:
            out[f.category] = out.get(f.category, 0) + 1
        return out


def _load_rules(path: Optional[Path] = None) -> List[dict]:
    with open(path or _REGISTRY_PATH, encoding="utf-8") as fh:
        return json.load(fh).get("rules", [])


_RULES_CACHE: Optional[List[tuple]] = None


def _compiled(path: Optional[Path] = None):
    global _RULES_CACHE
    if _RULES_CACHE is None or path is not None:
        compiled = [(re.compile(r["pattern"], re.IGNORECASE | re.MULTILINE), r) for r in _load_rules(path)]
        if path is None:
            _RULES_CACHE = compiled
        return compiled
    return _RULES_CACHE


def _effective_tier(rule: dict, doc_category: Optional[str]) -> Optional[str]:
    """Return the effective tier for this rule given the document category, or
    None if the rule does not apply here."""
    tier = rule.get("tier", "example")
    scope = rule.get("scope")
    if scope is None:
        return tier
    if doc_category is None:
        return "example"                      # scoped hard rule, unknown context -> advisory
    return tier if doc_category == scope else None   # out of scope -> does not fire


def lint_text(text: str, doc_category: Optional[str] = None, path: Optional[Path] = None) -> LintReport:
    """Scan text for registry constructions. ``doc_category`` (e.g. 'consent')
    scopes context-dependent hard rules such as the 21 CFR 50.20 patterns."""
    report = LintReport(words=len(re.findall(r"\b\w+\b", text)))
    line_starts = [0]
    for m in re.finditer(r"\n", text):
        line_starts.append(m.end())

    def locate(pos: int):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, pos - line_starts[lo] + 1

    for rx, rule in _compiled(path):
        tier = _effective_tier(rule, doc_category)
        if tier is None:
            continue
        for m in rx.finditer(text):
            line, col = locate(m.start())
            report.findings.append(
                LintFinding(
                    rule_id=rule["id"], category=rule["category"], severity=rule["severity"],
                    tier=tier, line=line, col=col, match_text=m.group(0).strip(),
                    message=rule["message"], suggestion=rule["suggestion"],
                    citation=rule.get("citation", ""),
                )
            )
    # hard-rule findings first, then by severity, then position
    report.findings.sort(key=lambda f: (f.tier != "hard-rule", -_SEVERITY_WEIGHT.get(f.severity, 1), f.line, f.col))
    return report


def lint_document(doc, doc_category: Optional[str] = None, path: Optional[Path] = None) -> LintReport:
    """Lint a generated Document's rendered text. Pass the document's registry
    category (e.g. 'consent') so scoped hard rules apply in context."""
    return lint_text(getattr(doc, "rendered", "") or "", doc_category=doc_category, path=path)


def format_report(report: LintReport) -> str:
    hard, ex = report.hard_findings, report.example_findings
    if not report.findings:
        return "register: CLEAN (%d words, 0 findings)" % report.words
    verdict = "PASS (no hard-rule findings)" if report.passes() else "FAIL (%d hard-rule)" % len(hard)
    lines = ["register: %d hard-rule + %d example finding(s); example density %.2f/1k -> %s"
             % (len(hard), len(ex), report.example_density_per_1k, verdict)]
    for f in report.findings:
        cite = (" <%s>" % f.citation) if f.citation else ""
        lines.append("  [%s/%s] L%d:%d %r (%s)%s -> %s"
                     % (f.tier, f.severity, f.line, f.col, f.match_text, f.message, cite, f.suggestion))
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cat = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--category=")), None)
    src = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
    print(format_report(lint_text(src, doc_category=cat)))
