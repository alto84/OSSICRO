"""CHECK pass: the completeness ledger and cross-document consistency.

The ledger is the operating definition of COMPLETE documentation
(strategy item 5): every required document resolves to exactly one of

  green - present, all required fields filled, validation rules pass,
          and any gate has a recorded human sign-off
  amber - present and complete, but a non-delegable gate is awaiting a
          qualified human (the engine can never clear this itself)
  awaiting-external-party - the drafted content is complete, but the
          real-world instrument is authored/signed by an EXTERNAL party
          (registry ``author_party`` != physician, Overhaul P4 / M2) and
          its receipt has not been recorded as a fact. Intake
          completeness alone can never turn such a document green.
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

# Overhaul P4 (M2): the fourth ledger state. A document whose real-world
# instrument an external party authors/signs can be drafted and internally
# complete, yet it is never DONE until the received, signed instrument is
# recorded as a fact.
AWAITING_EXTERNAL_PARTY = "awaiting-external-party"

# Overhaul P4 (M2): the external-party receipt-fact contract. For each
# external-authored document that has a recorded-receipt intake contract,
# the dotted study-record paths of the receipt facts. The LOA is the first
# (and currently only) such contract: the P2 fields
# manufacturer.loa_received_date / loa_signatory / loa_document_sha256.
# The presence of BOTH the date and the signatory turns the row green; the
# document hash is optional corroboration carried into the note.
EXTERNAL_RECEIPT_FACTS: Dict[str, Dict[str, str]] = {
    "manufacturer-letter-of-authorization": {
        "date": "manufacturer.loa_received_date",
        "signatory": "manufacturer.loa_signatory",
        "document_sha256": "manufacturer.loa_document_sha256",
        "party": "manufacturer",
        "question": (
            "Record the received, signed LOA (date + signatory) when the "
            "manufacturer issues it — the letter shown here is OSSICRO's "
            "draft for their review."
        ),
    },
}

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

        title = entry.get("title", doc_id)
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

        completeness_note = ("present; %d/%d required fields filled; validated"
                             % (len(entry.get("required_fields", [])),
                                len(entry.get("required_fields", []))))

        # AWAITING-EXTERNAL-PARTY (Overhaul P4 / M2): a document whose
        # real-world instrument an external party authors/signs can never be
        # green on intake completeness alone. It turns green only on a
        # RECORDED receipt fact (for the LOA: received date + signatory) or,
        # for gated external documents, the recorded human sign-off already
        # checked above.
        author_party = entry.get("author_party", "physician")
        if author_party != "physician" and not (gate_id and doc.has_signoff(gate_id)):
            facts = EXTERNAL_RECEIPT_FACTS.get(doc_id)
            received_date = study.resolve(facts["date"]) if facts else None
            signatory = study.resolve(facts["signatory"]) if facts else None
            if facts and received_date and signatory:
                receipt_note = (
                    "received, signed instrument recorded: %s, %s"
                    % (signatory, received_date))
                doc_hash = study.resolve(facts["document_sha256"])
                if doc_hash:
                    receipt_note += "; document sha256 %s" % doc_hash
                ledger.append(
                    LedgerItem(
                        doc_id=doc_id, title=title, status="green",
                        gate_id=gate_id,
                        notes=[completeness_note, receipt_note],
                    )
                )
            else:
                if facts:
                    question = facts["question"]
                else:
                    question = (
                        "'%s' is authored/signed by the %s, not the physician "
                        "— intake completeness alone cannot finish it. Record "
                        "the received instrument when the %s issues it."
                        % (title, author_party, author_party))
                ledger.append(
                    LedgerItem(
                        doc_id=doc_id, title=title,
                        status=AWAITING_EXTERNAL_PARTY,
                        gate_id=gate_id,
                        questions=[question],
                        notes=[completeness_note],
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
                notes=[completeness_note],
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
    # Four buckets from Overhaul P4 on: awaiting-external-party is a distinct
    # state, never folded into amber (a pending EXTERNAL act is not a pending
    # physician gate) and never hidden in green.
    totals = {"green": 0, "amber": 0, AWAITING_EXTERNAL_PARTY: 0, "red": 0}
    for item in ledger:
        totals[item.status] = totals.get(item.status, 0) + 1
    return totals
