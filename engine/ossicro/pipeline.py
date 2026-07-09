"""PIPELINE: cheapest-first, escalate-only composition of every check layer.

``run_check`` runs the layers in ascending cost and lets each ADD severity but
never remove it:

1. deterministic + provenance rules  (validate.run_rules)        -- microseconds
2. completeness ledger               (check.build_ledger)         -- fact-shaped
3. cross-document consistency        (check.check_consistency)    -- fact-shaped
4. register tripwire, per document   (register_linter.lint_document)
5. concept reviewer, per document    (review_port, default stub)  -- judgment

The ordering encodes the philosophy (docs/VALIDATION-PHILOSOPHY.md): rules and
the ledger are the cheap, predictable fact-shaped spine; the tripwire is a fast
fallible smoke signal; the concept reviewer is the expensive judgment layer that
improves as the model improves. The layers compose in ONE direction only.

Escalate-only coupling -- the hard invariant:
- a hard tripwire finding or a 'deficient' concept finding can turn an item RED
  and attach its resolving question;
- advisory findings attach ledger notes;
- NOTHING here clears a gate. An amber (gate-pending) item is never promoted to
  green by a clean review; a red item is never turned green. The gate packet is
  computed from the documents' recorded sign-offs, not from any finding.

``check.py`` is imported and composed, never modified.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .check import build_ledger, check_consistency
from .check import Inconsistency  # noqa: F401  (re-exported for callers)
from .models import Document, Gate, LedgerItem, Study
from .register_linter import LintReport, lint_document
from .review_port import (
    ConceptReviewer,
    DeterministicStubReviewer,
    ReviewReport,
    load_writing_principles,
    validate_report,
)
from .validate import RuleResult, run_rules

__all__ = ["CheckResult", "PendingGate", "run_check"]


@dataclass
class PendingGate:
    """A non-delegable gate still awaiting a named human, surfaced for routing."""

    gate_id: str
    name: str
    responsible_role: str
    citation: str
    doc_ids: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)


@dataclass
class CheckResult:
    ledger: List[LedgerItem]
    rule_results: List[RuleResult]
    inconsistencies: List["Inconsistency"]
    tripwire_by_doc: Dict[str, LintReport]
    concept_by_doc: Dict[str, ReviewReport]
    gate_packet: List[PendingGate]


def run_check(
    study: Study,
    documents: Dict[str, Document],
    doc_registry: Dict[str, dict],
    gate_registry: Dict[str, Gate],
    reviewer: Optional[ConceptReviewer] = None,
) -> CheckResult:
    """Compose all check layers over ``documents`` into a single CheckResult."""
    reviewer = reviewer or DeterministicStubReviewer()
    principles = load_writing_principles()

    # 1-3: fact-shaped spine (unchanged functions from check.py / validate.py)
    rule_results = run_rules(study, documents)
    inconsistencies = check_consistency(study, documents)
    base_ledger = build_ledger(study, documents, doc_registry, rule_results, inconsistencies)

    # 4: register tripwire per document, scoped by its registry category
    tripwire_by_doc: Dict[str, LintReport] = {}
    for doc_id, doc in documents.items():
        category = doc_registry.get(doc_id, {}).get("category")
        tripwire_by_doc[doc_id] = lint_document(doc, doc_category=category)

    # 5: concept reviewer per document, then defensively validated
    concept_by_doc: Dict[str, ReviewReport] = {}
    for doc_id, doc in documents.items():
        raw = reviewer.review(getattr(doc, "rendered", "") or "", doc, principles)
        concept_by_doc[doc_id] = validate_report(raw, doc)

    # Fold tripwire + concept findings into the ledger (escalate-only).
    ledger = _fold_findings(base_ledger, tripwire_by_doc, concept_by_doc)

    gate_packet = _gate_packet(ledger, documents, gate_registry, rule_results)

    return CheckResult(
        ledger=ledger,
        rule_results=rule_results,
        inconsistencies=inconsistencies,
        tripwire_by_doc=tripwire_by_doc,
        concept_by_doc=concept_by_doc,
        gate_packet=gate_packet,
    )


def _fold_findings(
    base_ledger: List[LedgerItem],
    tripwire_by_doc: Dict[str, LintReport],
    concept_by_doc: Dict[str, ReviewReport],
) -> List[LedgerItem]:
    """Return a new ledger with tripwire/concept findings folded in.

    Escalate-only: a hard tripwire finding or a deficient concept finding turns
    the item red and appends its resolving question; advisory findings append
    notes. The gate_id is always preserved, and no status ever moves toward
    green (amber and red are terminal-for-this-pass; only red can be ADDED).
    """
    folded: List[LedgerItem] = []
    for item in base_ledger:
        trip = tripwire_by_doc.get(item.doc_id)
        concept = concept_by_doc.get(item.doc_id)

        hard_questions: List[str] = []
        notes: List[str] = []

        if trip is not None:
            for f in trip.hard_findings:
                hard_questions.append(
                    "Register hard-rule [%s] at L%d:%d %r -- %s (%s). %s"
                    % (f.rule_id, f.line, f.col, f.match_text, f.message,
                       f.citation or "no citation", f.suggestion)
                )
            for f in trip.example_findings:
                notes.append(
                    "voice advisory [%s] %r: %s -> %s"
                    % (f.rule_id, f.match_text, f.message, f.suggestion)
                )

        if concept is not None:
            for f in concept.hard_findings:
                hard_questions.append(
                    "Concept review (%s) deficient against %s: %r -- %s. Rewrite: %s"
                    % (concept.model, f.principle_id, f.span, f.message, f.suggestion or "(none)")
                )
            for f in concept.advisory_findings:
                notes.append(
                    "concept advisory %s %r: %s"
                    % (f.principle_id, f.span, f.message)
                )

        # Escalate-only status resolution.
        new_status = item.status
        new_questions = list(item.questions)
        if hard_questions:
            new_status = "red"                       # amber/green -> red is escalation
            new_questions.extend(hard_questions)     # red stays red, question added

        folded.append(
            LedgerItem(
                doc_id=item.doc_id,
                title=item.title,
                status=new_status,
                questions=new_questions,
                gate_id=item.gate_id,                # gate never dropped
                notes=list(item.notes) + notes,
            )
        )
    return folded


def _gate_packet(
    ledger: List[LedgerItem],
    documents: Dict[str, Document],
    gate_registry: Dict[str, Gate],
    rule_results: List[RuleResult],
) -> List[PendingGate]:
    """Every non-delegable gate still awaiting a human, regardless of ledger color.

    Derived from the documents' recorded sign-offs (fact) and the unresolved
    SAE-causality rule -- NOT from any concept/tripwire finding. A concept
    finding can never add or clear a gate here.
    """
    pending: Dict[str, PendingGate] = {}

    def _ensure(gate_id: str) -> Optional[PendingGate]:
        if gate_id in pending:
            return pending[gate_id]
        gate = gate_registry.get(gate_id)
        if gate is None:
            return None
        pg = PendingGate(
            gate_id=gate.id,
            name=gate.name,
            responsible_role=gate.responsible_role,
            citation=gate.citation,
        )
        pending[gate_id] = pg
        return pg

    for item in ledger:
        if not item.gate_id:
            continue
        doc = documents.get(item.doc_id)
        if doc is not None and doc.has_signoff(item.gate_id):
            continue  # gate already executed by a human; not pending
        pg = _ensure(item.gate_id)
        if pg is not None:
            pg.doc_ids.append(item.doc_id)

    # Study-level SAE causality: a serious report with no human determination.
    for r in rule_results:
        if r.rule_id.startswith("R-SAE") and not r.passed:
            pg = _ensure("sae-causality")
            if pg is not None and r.resolving_question:
                pg.questions.append(r.resolving_question)

    return list(pending.values())
