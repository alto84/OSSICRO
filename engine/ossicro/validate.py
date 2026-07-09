"""VALIDATE pass: a small rule engine.

Each rule maps a (document/field) condition to pass/fail plus the
governing citation. Rules NEVER auto-resolve a gate: a rule that touches
an accountable act fails toward the gate (with a resolving question that
routes to the responsible human), it never executes the act.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from .models import Document, Study

# check functions return (passed, message, resolving_question_or_None)
CheckFn = Callable[[Study, Optional[Document]], Tuple[bool, str, Optional[str]]]


@dataclass
class Rule:
    id: str
    description: str
    citation: str
    doc_id: Optional[str]  # None = study-level rule
    fn: CheckFn


@dataclass
class RuleResult:
    rule_id: str
    doc_id: Optional[str]
    passed: bool
    message: str
    citation: str
    resolving_question: Optional[str] = None


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def _rule_1572_lists_irb(study: Study, doc: Optional[Document]):
    name = (doc.fields.get("irb_name", "") if doc else "").strip()
    if name:
        return True, "Form 1572 item 5 names the reviewing IRB: %s" % name, None
    return (
        False,
        "Form 1572 does not name a reviewing IRB (item 5).",
        "Which IRB (name and address) will review and approve this study? "
        "Enter it on Form 1572 item 5 (21 CFR 312.53(c)(1)(iv)).",
    )


def _rule_1572_phase_stated(study: Study, doc: Optional[Document]):
    phase = (doc.fields.get("phase", "") if doc else "").strip()
    if phase in {"1", "2", "3", "1/2", "2/3", "1b/2", "2a", "2b"}:
        return True, "Form 1572 item 8 states the investigation phase: %s" % phase, None
    return (
        False,
        "Form 1572 item 8 phase is missing or unrecognized: %r" % phase,
        "What phase of clinical investigation will be conducted? State it on "
        "Form 1572 item 8 (21 CFR 312.53(c)(1)(vii)).",
    )


def _rule_1571_30_day_clock(study: Study, doc: Optional[Document]):
    text = doc.rendered if doc else ""
    if "30 days" in text and "312.40" in text:
        return True, "Form 1571 carries the 30-day-wait commitment note.", None
    return (
        False,
        "Form 1571 lacks the 30-day IND wait commitment.",
        "Restore the sponsor commitment not to begin clinical investigations "
        "until 30 days after FDA receipt of the IND (21 CFR 312.40(b)(1)).",
    )


_ICF_ELEMENT_MARKERS = ["50.25(a)(%d)" % i for i in range(1, 9)]


def _rule_icf_eight_elements(study: Study, doc: Optional[Document]):
    text = doc.rendered if doc else ""
    missing = [m for m in _ICF_ELEMENT_MARKERS if m not in text]
    if not missing:
        return True, "ICF contains all 8 basic elements of 21 CFR 50.25(a).", None
    return (
        False,
        "ICF is missing basic consent element(s): %s" % ", ".join(missing),
        "Add the missing basic element(s) of informed consent (%s) to the ICF "
        "(21 CFR 50.25(a))." % ", ".join(missing),
    )


def _rule_delegation_log_names_pi(study: Study, doc: Optional[Document]):
    name = (doc.fields.get("investigator_name", "") if doc else "").strip()
    if name and name == study.investigator.name:
        return True, "Delegation log names the PI of record: %s" % name, None
    if name:
        return (
            False,
            "Delegation log PI (%r) does not match the study PI of record (%r)."
            % (name, study.investigator.name),
            "Who is the principal investigator of record? Reconcile the "
            "delegation log with the study record (ICH E6(R3) 2.7).",
        )
    return (
        False,
        "Delegation log does not name a principal investigator.",
        "Name the principal investigator on the delegation log "
        "(ICH E6(R3) 2.7; supervision is non-delegable under 21 CFR 312.60).",
    )


def _rule_protocol_versioned(study: Study, doc: Optional[Document]):
    if doc and doc.fields.get("protocol_version", "").strip() and doc.fields.get("protocol_date", "").strip():
        return True, "Protocol carries version and date identifiers.", None
    return (
        False,
        "Protocol lacks a version and/or date identifier.",
        "Assign the protocol a version number and date (ICH M11; "
        "ICH E6(R3) Appendix B) so amendments are traceable under 21 CFR 312.30.",
    )


def _rule_sae_causality_is_human(study: Study, doc: Optional[Document]):
    """Every serious safety report needs a HUMAN causality determination.

    This rule never fills the determination -- it fails toward the
    'sae-causality' gate. That is the never-auto-resolve behavior.
    """
    pending = [r for r in study.safety_reports if r.serious and r.causality_determination is None]
    if not pending:
        return True, "No serious safety report is awaiting a causality determination.", None
    ids = ", ".join(r.report_id for r in pending)
    return (
        False,
        "%d serious safety report(s) awaiting human causality/expectedness "
        "determination: %s. The engine computes deadlines only; it never "
        "makes this call." % (len(pending), ids),
        "Medical monitor: is there a reasonable possibility the drug caused "
        "the event(s) (%s), and is each event unexpected per the IB? "
        "(21 CFR 312.32(a)-(c); gate 'sae-causality')." % ids,
    )


RULES: List[Rule] = [
    Rule(
        id="R-1572-IRB",
        description="Form 1572 must list the reviewing IRB",
        citation="21 CFR 312.53(c)(1)(iv)",
        doc_id="form-fda-1572-statement-of-investigator",
        fn=_rule_1572_lists_irb,
    ),
    Rule(
        id="R-1572-PHASE",
        description="Form 1572 must state the phase of investigation",
        citation="21 CFR 312.53(c)(1)(vii)",
        doc_id="form-fda-1572-statement-of-investigator",
        fn=_rule_1572_phase_stated,
    ),
    Rule(
        id="R-1571-30DAY",
        description="IND cover must carry the 30-day clock commitment",
        citation="21 CFR 312.40(b)(1)",
        doc_id="form-fda-1571-ind-cover",
        fn=_rule_1571_30_day_clock,
    ),
    Rule(
        id="R-ICF-50.25",
        description="ICF must contain the 8 basic elements of informed consent",
        citation="21 CFR 50.25(a)(1)-(8)",
        doc_id="informed-consent-form-part50",
        fn=_rule_icf_eight_elements,
    ),
    Rule(
        id="R-DOA-PI",
        description="Delegation log must name the PI of record",
        citation="ICH E6(R3) 2.7; 21 CFR 312.60",
        doc_id="delegation-of-authority-log",
        fn=_rule_delegation_log_names_pi,
    ),
    Rule(
        id="R-PROT-VERSION",
        description="Protocol must carry version and date identifiers",
        citation="ICH M11; ICH E6(R3) Appendix B",
        doc_id="clinical-protocol-ich-m11-ceshharp",
        fn=_rule_protocol_versioned,
    ),
    Rule(
        id="R-SAE-CAUSALITY",
        description="Serious safety reports require a human causality determination (never auto-resolved)",
        citation="21 CFR 312.32(a)-(c); ICH E2A",
        doc_id=None,  # study-level
        fn=_rule_sae_causality_is_human,
    ),
]


def run_rules(study: Study, documents: Dict[str, Document]) -> List[RuleResult]:
    """Run every applicable rule. Document rules only run when the target
    document is present (its absence is the ledger's red, not a rule fail)."""
    results: List[RuleResult] = []
    for rule in RULES:
        if rule.doc_id is not None:
            doc = documents.get(rule.doc_id)
            if doc is None:
                continue
            passed, message, question = rule.fn(study, doc)
        else:
            passed, message, question = rule.fn(study, None)
        results.append(
            RuleResult(
                rule_id=rule.id,
                doc_id=rule.doc_id,
                passed=passed,
                message=message,
                citation=rule.citation,
                resolving_question=question,
            )
        )
    return results
