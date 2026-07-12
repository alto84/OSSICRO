"""Core data model for the OSSICRO engine.

Pure stdlib dataclasses. The Document state machine and the GateViolation
exception are the structural half of the HARD LINE: a Document whose
registry entry names a non-delegable gate cannot reach state 'final'
without a recorded human sign-off (see ossicro.gates).
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DOCUMENT_STATES = ("draft", "in_review", "approved", "final")

# Legal state transitions. 'final' is terminal.
_ALLOWED_TRANSITIONS = {
    "draft": {"in_review"},
    "in_review": {"draft", "approved"},
    "approved": {"draft", "final"},
    "final": set(),
}

# m8 (Overhaul P5): the capability token that authorizes moving a GATED
# document to 'final'. Held only by ossicro.gates.finalize, which verifies a
# VALID recorded human sign-off first. Document.advance("final") on a gated
# document refuses OUTRIGHT without it — finalize() is the only path to
# 'final' by code, not by convention.
_GATED_FINAL_TOKEN = object()


class StateError(RuntimeError):
    """Raised on an illegal Document state transition."""


class GateViolation(RuntimeError):
    """Raised when software attempts to execute a non-delegable human act.

    This exception firing is correct behavior, not an error condition to
    be worked around: it is the engine refusing to cross the hard line.
    """


def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ProvenanceRecord:
    """Where a filled span came from and what authority governs it."""

    span: str        # the template field / text span that was filled
    source: str      # the structured-data path and value that filled it
    citation: str    # governing CFR/ICH/form authority for the span
    input_hash: str = ""  # sha256 of the canonicalized intake consumed by the
                          # generation that produced this record (INV-3).
                          # "" = pre-INV-3 record or engine-only test path.


@dataclass
class StudyFact:
    """A provenance-stamped study-record fact (StudyFacts v0).

    The canonical fact spine the generators consume: every value carries
    where it came from and who (if anyone) attested it. Empty
    ``attested_by``/``date`` means the datum entered at study-record
    intake without a recorded attestation -- honestly unattested, never
    fabricated.
    """

    value: str
    source: str          # dotted path into the raw study record, e.g. 'investigator.name'
    attested_by: str = ""  # named human who attested the value ('' = unattested intake)
    date: str = ""         # attestation/collection date ('' = unrecorded)


@dataclass
class HumanSignoff:
    """A recorded human execution of a non-delegable gate.

    In production this is an authenticated Part 11 e-signature record
    (21 CFR 11.50-11.300). The prototype records attribution only.

    ``evidence`` (M13, Overhaul P5) carries the sign-off's supporting facts
    as entered by the signer — e.g. for irb-approval
    ``{concurrence_date, concurring_member, irb_reference}``, for
    informed-consent ``{consent_date}``. Keys may be honestly blank; the
    record never invents them.
    """

    gate_id: str
    person: str
    role: str
    statement: str
    timestamp: str = field(default_factory=_utcnow)
    evidence: Dict[str, str] = field(default_factory=dict)


@dataclass
class Gate:
    """A non-delegable function that must be executed by a named human.

    ``responsible_role`` is the ROLE-MATCHING KEY a sign-off must carry;
    ``responsible_role_label`` (m1, Overhaul P5) is an optional DISPLAY
    label for surfaces a human reads (e.g. sae-causality shows
    "physician-sponsor / medical monitor" while the key stays
    "medical-monitor"). Empty label = display the key.
    """

    id: str
    name: str
    description: str
    responsible_role: str
    citation: str
    responsible_role_label: str = ""

    @property
    def role_label(self) -> str:
        """The human-facing role label (falls back to the matching key)."""
        return self.responsible_role_label or self.responsible_role


@dataclass
class Person:
    name: str
    role: str = ""
    phone: str = ""
    email: str = ""


@dataclass
class Investigator:
    name: str
    degrees: str = ""
    address: str = ""
    license_number: str = ""
    license_state: str = ""
    phone: str = ""


@dataclass
class Site:
    name: str
    address: str = ""
    clinical_lab_name: str = ""
    clinical_lab_address: str = ""


@dataclass
class SafetyReport:
    """A serious-adverse-event record.

    ``causality_determination`` and ``expectedness_determination`` hold a
    HumanSignoff or None. The engine never sets them; use
    ossicro.gates.record_causality_determination, which verifies the
    responsible role. A None value routes the report to the
    'sae-causality' gate in the ledger and compliance map.
    """

    report_id: str
    subject_code: str
    event_term: str
    onset_date: str
    serious: bool = True
    seriousness_criteria: str = ""
    causality_determination: Optional[HumanSignoff] = None
    expectedness_determination: Optional[HumanSignoff] = None


@dataclass
class LedgerItem:
    """One row of the completeness ledger.

    status: 'green'  - present, all required fields filled, validated
            'amber'  - present and complete but awaiting a non-delegable
                       human gate
            'awaiting-external-party' - drafted and complete, but the
                       real-world instrument is authored/signed by an
                       external party (registry author_party, Overhaul
                       P4/M2) and its receipt is not yet recorded
            'red'    - missing document, missing required field, failed
                       validation, or cross-document inconsistency; the
                       exact resolving question(s) are attached
    """

    doc_id: str
    title: str
    status: str
    questions: List[str] = field(default_factory=list)
    gate_id: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    @property
    def resolving_question(self) -> Optional[str]:
        return self.questions[0] if self.questions else None


@dataclass
class Document:
    """A generated or collected regulatory document.

    State machine: draft -> in_review -> approved -> final.
    Every filled field carries a ProvenanceRecord in ``provenance``.
    If ``gate_id`` is set, transition to 'final' requires a recorded
    HumanSignoff for that gate (enforced here AND in ossicro.gates).
    """

    doc_id: str
    title: str
    state: str = "draft"
    fields: Dict[str, str] = field(default_factory=dict)
    provenance: List[ProvenanceRecord] = field(default_factory=list)
    rendered: str = ""
    gate_id: Optional[str] = None
    signoffs: List[HumanSignoff] = field(default_factory=list)
    input_hash: str = ""  # sha256 of the canonicalized intake this document
                          # was generated from (INV-3; package-manifest grain)

    def has_signoff(self, gate_id: str) -> bool:
        return any(s.gate_id == gate_id for s in self.signoffs)

    def advance(self, to_state: str, *, _finalize_token: object = None) -> None:
        """Advance the document state machine.

        m8 (Overhaul P5): for a GATED document, ``advance("final")`` refuses
        OUTRIGHT — even with a recorded sign-off. ``ossicro.gates.finalize``
        (which verifies a VALID sign-off and holds the module-private
        capability token) is the only path to 'final', by code instead of
        by convention.
        """
        if to_state not in DOCUMENT_STATES:
            raise StateError("Unknown document state: %r" % to_state)
        if to_state not in _ALLOWED_TRANSITIONS.get(self.state, set()):
            raise StateError(
                "Illegal transition %s -> %s for %s"
                % (self.state, to_state, self.doc_id)
            )
        if (to_state == "final" and self.gate_id
                and _finalize_token is not _GATED_FINAL_TOKEN):
            raise GateViolation(
                "Document '%s' is gated by non-delegable gate '%s': "
                "advance('final') is refused outright for gated documents "
                "(m8). ossicro.gates.finalize is the only path to 'final' — "
                "it verifies the recorded human sign-off; it never creates one."
                % (self.doc_id, self.gate_id)
            )
        self.state = to_state


@dataclass
class Study:
    """The structured study record all documents are generated from.

    ``raw`` retains the full fixture dict; ``resolve`` walks it with a
    dotted path ('investigator.name') and is the single source used by
    generation, so every provenance record traces to a raw-data path.
    """

    raw: Dict[str, Any]
    study_id: str
    title: str
    phase: str
    protocol_number: str
    protocol_version: str
    ind_number: str
    investigator: Investigator
    site: Site
    irb: Dict[str, str]
    required_documents: List[str] = field(default_factory=list)
    safety_reports: List[SafetyReport] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "Study":
        inv = raw.get("investigator", {})
        site = raw.get("site", {})
        lab = site.get("clinical_lab", {})
        reports = [
            SafetyReport(
                report_id=r.get("report_id", ""),
                subject_code=r.get("subject_code", ""),
                event_term=r.get("event_term", ""),
                onset_date=r.get("onset_date", ""),
                serious=bool(r.get("serious", True)),
                seriousness_criteria=r.get("seriousness_criteria", ""),
            )
            for r in raw.get("safety_reports", [])
        ]
        return cls(
            raw=raw,
            study_id=raw.get("study_id", ""),
            title=raw.get("title", ""),
            phase=str(raw.get("phase", "")),
            protocol_number=raw.get("protocol_number", ""),
            protocol_version=raw.get("protocol_version", ""),
            ind_number=raw.get("ind_number", ""),
            investigator=Investigator(
                name=inv.get("name", ""),
                degrees=inv.get("degrees", ""),
                address=inv.get("address", ""),
                license_number=inv.get("license_number", ""),
                license_state=inv.get("license_state", ""),
                phone=inv.get("phone", ""),
            ),
            site=Site(
                name=site.get("name", ""),
                address=site.get("address", ""),
                clinical_lab_name=lab.get("name", ""),
                clinical_lab_address=lab.get("address", ""),
            ),
            irb=raw.get("irb", {}),
            required_documents=list(raw.get("required_documents", [])),
            safety_reports=reports,
        )

    def resolve(self, path: str) -> Optional[str]:
        """Resolve a dotted path against the raw study dict.

        Returns None if any segment is missing or the value is empty.
        """
        node: Any = self.raw
        for part in path.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None
        if node is None:
            return None
        if isinstance(node, (dict, list)):
            return None  # a path landing on a container is not a scalar value
        text = str(node).strip()
        return text if text else None

    def fact(self, path: str) -> Optional[StudyFact]:
        """Return the provenance-stamped StudyFact at a dotted path, or None.

        Wraps ``resolve`` (which stays the single raw-data walker):
        the fact's ``source`` is the path itself, and attestation
        metadata is read from ``raw['attestations'][path]`` when the
        intake record carries it, e.g.

            "attestations": {"phase": {"attested_by": "Jordan A. Rivera, MD",
                                       "date": "2026-07-01"}}

        Absent that, the fact is returned with empty attribution --
        marked unattested rather than invented.
        """
        value = self.resolve(path)
        if value is None:
            return None
        attestations = self.raw.get("attestations", {})
        meta = attestations.get(path, {}) if isinstance(attestations, dict) else {}
        if not isinstance(meta, dict):
            meta = {}
        return StudyFact(
            value=value,
            source=path,
            attested_by=str(meta.get("attested_by", "")).strip(),
            date=str(meta.get("date", "")).strip(),
        )
