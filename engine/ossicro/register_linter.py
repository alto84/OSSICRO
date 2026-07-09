"""REGISTER LINTER: the deterministic anti-AI-slop substrate.

A zero-LLM, versioned check that flags LLM mannerisms and promotional slop so
OSSICRO-generated documents read as professional regulatory work product. It
is deterministic (a regex registry, not a model), so its verdict is
reproducible and defensible; and it is FALSE-POSITIVE-CONTROLLED — legitimate
regulatory vocabulary is deliberately not on the list.

A finding is a flag for human review or an automated rewrite pass, never a
silent edit. The engine never changes a human-vetted verbatim passage.
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
    line: int
    col: int
    match_text: str
    message: str
    suggestion: str


@dataclass
class LintReport:
    findings: List[LintFinding] = field(default_factory=list)
    words: int = 0

    @property
    def weighted_score(self) -> int:
        return sum(_SEVERITY_WEIGHT.get(f.severity, 1) for f in self.findings)

    @property
    def density_per_1k(self) -> float:
        return round(1000.0 * self.weighted_score / self.words, 2) if self.words else 0.0

    def passes(self, max_high: int = 0, max_density: float = 4.0) -> bool:
        """A document passes if it has no high-severity slop and stays under a
        weighted-density ceiling (default: <=0 high findings, <4.0 per 1k words)."""
        highs = sum(1 for f in self.findings if f.severity == "high")
        return highs <= max_high and self.density_per_1k < max_density

    def by_category(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for f in self.findings:
            out[f.category] = out.get(f.category, 0) + 1
        return out


def _load_rules(path: Optional[Path] = None) -> List[dict]:
    with open(path or _REGISTRY_PATH, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("rules", [])


_RULES_CACHE: Optional[List[tuple]] = None


def _compiled(path: Optional[Path] = None):
    global _RULES_CACHE
    if _RULES_CACHE is None or path is not None:
        compiled = []
        for r in _load_rules(path):
            compiled.append((re.compile(r["pattern"], re.IGNORECASE | re.MULTILINE), r))
        if path is None:
            _RULES_CACHE = compiled
        return compiled
    return _RULES_CACHE


def lint_text(text: str, path: Optional[Path] = None) -> LintReport:
    """Scan text for banned constructions; return a LintReport."""
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
        for m in rx.finditer(text):
            line, col = locate(m.start())
            report.findings.append(
                LintFinding(
                    rule_id=rule["id"], category=rule["category"], severity=rule["severity"],
                    line=line, col=col, match_text=m.group(0).strip(),
                    message=rule["message"], suggestion=rule["suggestion"],
                )
            )
    report.findings.sort(key=lambda f: (-_SEVERITY_WEIGHT.get(f.severity, 1), f.line, f.col))
    return report


def lint_document(doc, path: Optional[Path] = None) -> LintReport:
    """Lint a generated Document's rendered text (see ossicro.models.Document)."""
    return lint_text(getattr(doc, "rendered", "") or "", path)


def format_report(report: LintReport) -> str:
    if not report.findings:
        return "register: CLEAN (%d words, 0 findings)" % report.words
    lines = ["register: %d finding(s), weighted density %.2f/1k words -> %s"
             % (len(report.findings), report.density_per_1k,
                "PASS" if report.passes() else "FAIL")]
    for f in report.findings:
        lines.append("  [%s] L%d:%d %r (%s) -> %s"
                     % (f.severity, f.line, f.col, f.match_text, f.message, f.suggestion))
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    print(format_report(lint_text(src)))
