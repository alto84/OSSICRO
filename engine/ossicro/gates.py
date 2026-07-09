"""Gate enforcement: the code-level HARD LINE.

Any Document whose registry entry names a non-delegable gate cannot
reach state 'final' without a recorded human sign-off. Attempting to
finalize programmatically raises GateViolation. Nothing in this module
(or anywhere in the engine) can execute a gate; it can only RECORD that
a qualified human executed it, with attribution.
"""

from __future__ import annotations

from typing import Dict, Optional

from .models import Document, Gate, GateViolation, HumanSignoff, SafetyReport

__all__ = [
    "GateViolation",
    "record_signoff",
    "finalize",
    "record_causality_determination",
]


def record_signoff(
    document: Document,
    gate_registry: Dict[str, Gate],
    person: str,
    role: str,
    statement: str,
    timestamp: Optional[str] = None,
) -> HumanSignoff:
    """Record that a named human executed the document's gate.

    Refuses if the document has no gate, if the gate is unknown, if the
    actor's role does not match the gate's responsible role, or if
    attribution is missing. In production this call sits behind an
    authenticated 21 CFR Part 11 e-signature ceremony; the prototype
    enforces attribution and role only.
    """
    if not document.gate_id:
        raise GateViolation(
            "Document '%s' has no gate; nothing to sign off." % document.doc_id
        )
    gate = gate_registry.get(document.gate_id)
    if gate is None:
        raise GateViolation("Unknown gate id %r." % document.gate_id)
    if not person or not person.strip():
        raise GateViolation(
            "A gate sign-off requires a named human. Gate '%s' (%s) must be "
            "executed by the %s." % (gate.id, gate.name, gate.responsible_role)
        )
    if role != gate.responsible_role:
        raise GateViolation(
            "Gate '%s' (%s) must be executed by role '%s', not '%s' "
            "(authority: %s)." % (gate.id, gate.name, gate.responsible_role, role, gate.citation)
        )
    if not statement or not statement.strip():
        raise GateViolation(
            "A gate sign-off requires the signer's attestation statement."
        )
    kwargs = {"timestamp": timestamp} if timestamp else {}
    signoff = HumanSignoff(
        gate_id=gate.id, person=person.strip(), role=role,
        statement=statement.strip(), **kwargs
    )
    document.signoffs.append(signoff)
    return signoff


def finalize(document: Document, gate_registry: Dict[str, Gate]) -> Document:
    """Advance a document to 'final'.

    Raises GateViolation if the document is gated and no human sign-off
    has been recorded. This is the only sanctioned path to 'final' for
    gated documents, and it cannot create the sign-off itself.
    """
    if document.gate_id and not document.has_signoff(document.gate_id):
        gate = gate_registry.get(document.gate_id)
        who = gate.responsible_role if gate else "the responsible human"
        why = gate.citation if gate else "governing authority"
        raise GateViolation(
            "REFUSED: '%s' is gated by '%s' -- a non-delegable act of the %s "
            "(%s). The engine drafts and validates; it never executes this. "
            "Record the human sign-off first (gates.record_signoff)."
            % (document.doc_id, document.gate_id, who, why)
        )
    document.advance("final")
    return document


def record_causality_determination(
    report: SafetyReport,
    gate_registry: Dict[str, Gate],
    person: str,
    role: str,
    statement: str,
) -> HumanSignoff:
    """Record a HUMAN causality/expectedness determination on an SAE.

    The engine never sets causality. This function only records that the
    medical monitor (the 'sae-causality' gate's responsible role) made
    the determination, with attribution.
    """
    gate = gate_registry.get("sae-causality")
    if gate is None:
        raise GateViolation("Gate registry is missing 'sae-causality'.")
    if not person or not person.strip():
        raise GateViolation(
            "Causality determination requires a named human (%s)."
            % gate.responsible_role
        )
    if role != gate.responsible_role:
        raise GateViolation(
            "Causality/expectedness on %s is the %s's non-delegable judgment "
            "(%s); role '%s' cannot record it."
            % (report.report_id, gate.responsible_role, gate.citation, role)
        )
    if not statement or not statement.strip():
        raise GateViolation(
            "Causality determination requires the determining physician's "
            "statement (the judgment itself must come from the human)."
        )
    signoff = HumanSignoff(
        gate_id=gate.id, person=person.strip(), role=role, statement=statement.strip()
    )
    report.causality_determination = signoff
    return signoff
