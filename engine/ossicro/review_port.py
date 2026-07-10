"""CONCEPT-REVIEWER PORT: judgment against stated principles.

This is the seam where OSSICRO's default validation posture -- concept-based
judgment (docs/VALIDATION-PHILOSOPHY.md) -- plugs in. A concept reviewer reads
a generated span and judges it against a cited *principle stated as text*, not a
frozen pattern. In production the reviewer is a Claude SDK agent running
Anthropic's critique-and-revise loop; here we define the port plus an offline,
deterministic stub so the pipeline and its tests run with no network.

Three invariants hold for every reviewer implementation:

1. **Span-scoped jurisdiction.** The reviewer judges filled field values and
   generated spans. Verbatim-locked and fixed template prose are outside its
   jurisdiction *by construction* -- enforced defensively by ``validate_report``,
   which DROPS any finding falling inside a verbatim-locked span. The reviewer
   can flag; it can never edit a locked span.
2. **Quote-what-exists.** A finding must quote text that actually appears in the
   document. ``validate_report`` drops a finding whose quoted span is not a
   verbatim substring of the rendered document -- defensive against a reviewer
   inventing evidence.
3. **Escalate-only.** A ReviewReport is advisory input to the pipeline. It can
   add reds or advisories, drive a rewrite, and open a gate earlier; it can
   never clear a gate, turn a red green, or alter a deadline. That coupling
   lives in ossicro.pipeline, not here.
"""

from __future__ import annotations

import abc
import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from .generate import VERBATIM_SPANS
from .register_linter import lint_text

# Concept-finding severities. 'deficient' is a hard finding (the pipeline may
# turn it into a red); 'advisory' is a non-blocking smoke signal (a ledger
# note). Mirrors the deficient | adequate | advisory grading in
# docs/VALIDATION-PHILOSOPHY.md §5; 'adequate' produces no finding at all.
HARD_SEVERITY = "deficient"
ADVISORY_SEVERITY = "advisory"


def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Principle:
    """One cited writing/validation principle, stated as text.

    The principle -- not a pattern -- is the check. ``source`` locates the
    governing rubric so a finding is auditable back to the standard it applies.
    """

    id: str
    text: str
    source: str


@dataclass
class ConceptFinding:
    """A single judgment against one principle, on one quoted span.

    ``span`` is the quoted evidence: verbatim text from the document. ``message``
    is the rationale; ``suggestion`` is the proposed rewrite. A finding never
    edits anything -- it routes to the human reviewer and the rewrite loop.
    """

    principle_id: str
    severity: str          # 'deficient' (hard) | 'advisory'
    span: str
    message: str
    suggestion: str = ""

    @property
    def is_hard(self) -> bool:
        return self.severity == HARD_SEVERITY


@dataclass
class ReviewReport:
    """The reviewer's structured output for one document.

    ``model`` records the reviewing model's identifier and ``reviewed_at`` the
    timestamp -- the Part 11 attribution substrate for every concept-layer
    contribution (docs/VALIDATION-PHILOSOPHY.md §5).

    ``error`` is set when the reviewer itself failed (exception, transport
    fault): the document is then UNREVIEWED, and the pipeline escalates that
    to a blocking red -- a reviewer failure can never silently pass a document.
    """

    findings: List[ConceptFinding] = field(default_factory=list)
    model: str = ""
    reviewed_at: str = field(default_factory=_utcnow)
    error: str = ""

    @property
    def hard_findings(self) -> List[ConceptFinding]:
        return [f for f in self.findings if f.is_hard]

    @property
    def advisory_findings(self) -> List[ConceptFinding]:
        return [f for f in self.findings if not f.is_hard]


# ---------------------------------------------------------------------------
# Writing principles (compact set derived from docs/WRITING-PRINCIPLES.md v1.0)
# ---------------------------------------------------------------------------

_WRITING_PRINCIPLES: List[Principle] = [
    Principle("P1", "Every sentence serves the reader's decision; a sentence that "
                    "could be deleted without changing what the reader can decide "
                    "should be deleted.", "docs/WRITING-PRINCIPLES.md#1"),
    Principle("P2", "Evidence over emphasis: state facts plainly. Importance claims "
                    "without content, promotional framing, and superlatives are "
                    "defects, severity-critical in consent and counterparty text.",
              "docs/WRITING-PRINCIPLES.md#2"),
    Principle("P3", "Calibrated uncertainty, stated once with its source; no stacked "
                    "modals, no false confidence.", "docs/WRITING-PRINCIPLES.md#3"),
    Principle("P4", "The document does not narrate itself: no metacommentary, no "
                    "framing of what it is about to do, no summaries of what it just "
                    "did.", "docs/WRITING-PRINCIPLES.md#4"),
    Principle("P5", "Register is per-document and per-audience; the same sentence can "
                    "be correct in one register and a defect in another.",
              "docs/WRITING-PRINCIPLES.md#5"),
    Principle("P6", "Write as the signer: a licensed physician would adopt this "
                    "sentence as their own professional work product.",
              "docs/WRITING-PRINCIPLES.md#6"),
    Principle("P7", "Precision beats variety: defined terms repeat verbatim; formal "
                    "passives, 'shall', and boilerplate are legitimate regulatory "
                    "register.", "docs/WRITING-PRINCIPLES.md#7"),
    Principle("P8", "Nothing reveals the drafting process: no chat residue, no AI "
                    "self-reference, no instruction leakage.",
              "docs/WRITING-PRINCIPLES.md#8"),
]

# lint-registry category -> the principle the mannerism most directly violates.
_CATEGORY_TO_PRINCIPLE = {
    "filler-hedge": "P4",
    "summary-slop": "P4",
    "transition-slop": "P4",
    "mannerism": "P2",
    "promotional": "P2",
    "wordiness": "P1",
    "chat-residue": "P8",
    "exculpatory-50.20": "P5",
}


def load_writing_principles() -> List[Principle]:
    """Return the writing-principles rubric the voice reviewer applies."""
    return list(_WRITING_PRINCIPLES)


# ---------------------------------------------------------------------------
# The port
# ---------------------------------------------------------------------------

class ConceptReviewer(abc.ABC):
    """Abstract concept reviewer. A production implementation wraps a model."""

    #: identifier recorded on every ReviewReport for the audit trail
    model: str = "abstract"

    @abc.abstractmethod
    def review(self, text: str, doc, principles: List[Principle]) -> ReviewReport:
        """Judge ``text`` (a document's rendered prose) against ``principles``.

        Returns a ReviewReport of findings. Implementations must not mutate
        ``doc`` -- the reviewer flags, it never edits.
        """
        raise NotImplementedError


class DeterministicStubReviewer(ConceptReviewer):
    """Offline, reproducible stand-in for the model-backed concept reviewer.

    It seeds its findings from the register-linter's tier-B example tripwires
    (docs/WRITING-PRINCIPLES.md's dated illustrative examples), so its output is
    deterministic and network-free -- exactly what tests need. A real reviewer
    replaces it with model judgment; the port, the ReviewReport shape, and the
    escalate-only coupling in the pipeline stay identical.

    Mapping: a high-severity example match becomes a 'deficient' concept finding
    (a defect a careful signer would not adopt); medium/low become 'advisory'.
    Scoped hard rules (e.g. 21 CFR 50.20) are left to the deterministic tripwire
    in the pipeline; this stub speaks only to voice.
    """

    model = "deterministic-stub-v0"

    def review(self, text: str, doc, principles: List[Principle]) -> ReviewReport:
        known_ids = {p.id for p in principles}
        report = ReviewReport(model=self.model)
        lint = lint_text(text or "")
        for f in lint.example_findings:
            principle_id = _CATEGORY_TO_PRINCIPLE.get(f.category, "P2")
            if principle_id not in known_ids:
                principle_id = "P2"
            severity = HARD_SEVERITY if f.severity == "high" else ADVISORY_SEVERITY
            report.findings.append(
                ConceptFinding(
                    principle_id=principle_id,
                    severity=severity,
                    span=f.match_text,
                    message=f.message,
                    suggestion=f.suggestion,
                )
            )
        return report


# ---------------------------------------------------------------------------
# Defensive validation of a report against the locked-span invariant
# ---------------------------------------------------------------------------

def _locked_ranges(doc) -> List[tuple]:
    """Character ranges in doc.rendered covered by verbatim-locked spans."""
    if doc is None:
        return []
    rendered = getattr(doc, "rendered", "") or ""
    ranges: List[tuple] = []
    for span_text, _citation in VERBATIM_SPANS.get(getattr(doc, "doc_id", ""), {}).values():
        start = rendered.find(span_text)
        while start != -1:
            ranges.append((start, start + len(span_text)))
            start = rendered.find(span_text, start + 1)
    return ranges


def validate_report(report: ReviewReport, doc) -> ReviewReport:
    """Drop findings the reviewer had no authority to make.

    A finding is dropped when either:
    - its quoted ``span`` does not appear verbatim in the rendered document
      (the reviewer quoted text that isn't there -- non-actionable / invented),
      or
    - the quoted span falls inside a verbatim-locked template span (outside the
      reviewer's jurisdiction by construction; it may flag but never touch a
      locked span).

    Returns a new ReviewReport preserving model/reviewed_at attribution.
    """
    rendered = getattr(doc, "rendered", "") or "" if doc is not None else ""
    locked = _locked_ranges(doc)
    kept: List[ConceptFinding] = []
    for f in report.findings:
        span = f.span or ""
        if not span:
            continue
        idx = rendered.find(span)
        if idx == -1:
            continue  # quotes text not present in the document
        end = idx + len(span)
        inside_locked = any(idx < lo_hi[1] and end > lo_hi[0] for lo_hi in locked)
        if inside_locked:
            continue  # locked span: reviewer may flag but never edit it
        kept.append(f)
    return ReviewReport(findings=kept, model=report.model,
                        reviewed_at=report.reviewed_at, error=report.error)
