"""CHECK pass: the completeness ledger and cross-document consistency.

The ledger is the operating definition of COMPLETE documentation
(strategy item 5): every required document resolves to exactly one of

  green - present, all required fields filled, validation rules pass,
          and any gate has a recorded human sign-off
  amber - present and complete, but a non-delegable gate is awaiting a
          qualified human (the engine can never clear this itself)
  red   - missing document, missing required field, failed validation
          rule, or cross-document inconsistency -- each with the exact
          resolving question a human can answer

The consistency check compares identity-critical fields (investigator
name, IND number, protocol number/version, title) across every document
that carries them, against the study record as reference (strategy
item 4: cross-document consistency engine).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .models import Document, LedgerItem, Study

# field name (as it appears in Document.fields) -> dotted study-record path
CONSISTENCY_KEYS: Dict[str, str] = {
    "investigator_name": "investigator.name",
    "ind_number": "ind_number",
    "protocol_number": "protocol_number",
    "protocol_version": "protocol_version",
    "protocol_title": "title",
}


@dataclass
class Inconsistency:
    """A cross-document mismatch on an identity-critical field."""

    field_name: str
    reference_value: str            # value in the study record
    observed: Dict[str, str] = field(default_factory=dict)  # doc_id -> deviating value
    question: str = ""

    def implicated_docs(self) -> List[str]:
        return sorted(self.observed)


def check_consistency(study: Study, documents: Dict[str, Document]) -> List[Inconsistency]:
    """Compare shared identity fields across all documents vs the study record."""
    findings: List[Inconsistency] = []
    for field_name, path in CONSISTENCY_KEYS.items():
        reference = study.resolve(path)
        if reference is None:
            continue
        deviations: Dict[str, str] = {}
        for doc_id, doc in documents.items():
            value = doc.fields.get(field_name)
            if value is not None and value.strip() and value.strip() != reference:
                deviations[doc_id] = value.strip()
        if deviations:
            findings.append(
                Inconsistency(
                    field_name=field_name,
                    reference_value=reference,
                    observed=deviations,
                    question=(
                        "'%s' differs across documents: study record says %r but %s. "
                        "Which value is current? Correct the stale artifact(s) before filing."
                        % (
                            field_name,
                            reference,
                            "; ".join(
                                "%s says %r" % (d, v) for d, v in sorted(deviations.items())
                            ),
                        )
                    ),
                )
            )
    return findings


def build_ledger(
    study: Study,
    documents: Dict[str, Document],
    doc_registry: Dict[str, dict],
    rule_results: Optional[list] = None,
    inconsistencies: Optional[List[Inconsistency]] = None,
) -> List[LedgerItem]:
    """Compute the completeness ledger over the study's required documents.

    ``rule_results`` (from ossicro.validate.run_rules) and
    ``inconsistencies`` (from check_consistency) are folded in when
    provided: a failed rule or an implicated inconsistency makes a
    document red with the corresponding resolving question.
    """
    rule_results = rule_results or []
    inconsistencies = inconsistencies or []
    failed_by_doc: Dict[str, List] = {}
    for r in rule_results:
        if not r.passed and r.doc_id:
            failed_by_doc.setdefault(r.doc_id, []).append(r)
    inconsistent_docs: Dict[str, List[Inconsistency]] = {}
    for finding in inconsistencies:
        for doc_id in finding.implicated_docs():
            inconsistent_docs.setdefault(doc_id, []).append(finding)

    ledger: List[LedgerItem] = []
    for doc_id in study.required_documents:
        entry = doc_registry.get(doc_id)
        if entry is None:
            ledger.append(
                LedgerItem(
                    doc_id=doc_id,
                    title=doc_id,
                    status="red",
                    questions=[
                        "Document id %r is not in the registry. Is the id correct, "
                        "or does the registry need a new entry?" % doc_id
                    ],
                )
            )
            continue

        title = entry["title"]
        gate_id = entry.get("gate")
        citations = entry.get("governing_citations", [])
        first_citation = citations[0] if citations else "governing authority"
        doc = documents.get(doc_id)

        # RED: document missing entirely
        if doc is None:
            ledger.append(
                LedgerItem(
                    doc_id=doc_id,
                    title=title,
                    status="red",
                    gate_id=gate_id,
                    questions=[
                        "'%s' is missing. Generate it, or collect it from its owner "
                        "(%s); required under %s." % (title, entry.get("owner", "?"), first_citation)
                    ],
                )
            )
            continue

        questions: List[str] = []

        # RED: missing required fields, each with the exact resolving question
        field_citations = _field_citation_lookup(doc_id)
        for field_name in entry.get("required_fields", []):
            if not doc.fields.get(field_name, "").strip():
                citation = field_citations.get(field_name, first_citation)
                questions.append(
                    "Provide '%s' for %s (required by %s)." % (field_name, title, citation)
                )

        # RED: failed validation rules
        for r in failed_by_doc.get(doc_id, []):
            if r.resolving_question:
                questions.append(r.resolving_question)

        # RED: cross-document inconsistency implicating this document
        for finding in inconsistent_docs.get(doc_id, []):
            questions.append(finding.question)

        if questions:
            ledger.append(
                LedgerItem(
                    doc_id=doc_id, title=title, status="red",
                    gate_id=gate_id, questions=questions,
                )
            )
            continue

        # AMBER: complete but awaiting the non-delegable human gate
        if gate_id and not doc.has_signoff(gate_id):
            ledger.append(
                LedgerItem(
                    doc_id=doc_id,
                    title=title,
                    status="amber",
                    gate_id=gate_id,
                    questions=[
                        "Awaiting non-delegable human act: gate '%s' must be executed "
                        "by the responsible human (see gates registry). The engine "
                        "cannot and will not clear this." % gate_id
                    ],
                )
            )
            continue

        # GREEN
        ledger.append(
            LedgerItem(
                doc_id=doc_id,
                title=title,
                status="green",
                gate_id=gate_id,
                notes=["present; %d/%d required fields filled; validated"
                       % (len(entry.get("required_fields", [])),
                          len(entry.get("required_fields", [])))],
            )
        )
    return ledger


def _field_citation_lookup(doc_id: str) -> Dict[str, str]:
    """Per-field citations for built-in templates (best-effort elsewhere)."""
    try:
        from .generate import FIELD_SOURCES
        return {f: cit for f, (_, cit) in FIELD_SOURCES.get(doc_id, {}).items()}
    except ImportError:  # pragma: no cover
        return {}


def ledger_totals(ledger: List[LedgerItem]) -> Dict[str, int]:
    totals = {"green": 0, "amber": 0, "red": 0}
    for item in ledger:
        totals[item.status] = totals.get(item.status, 0) + 1
    return totals
