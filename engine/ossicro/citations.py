"""Single-source statutory-citation table (Overhaul P1, [PT-2]).

Every regulatory pinpoint the generators, templates, registries, and the app
emit for the 21 CFR 312.305(b)(2) content family and the statutory clocks is
looked up HERE by content key — never string-literal'd twice. From Package 1
on, no NEW pinpoint may bypass this table; the remaining legacy citations
migrate opportunistically in later packages.

Human-verification discipline (HITL — Constitution: never silently asserted
final):

- Every row carries a status: ``HUMAN-VERIFIED`` or
  ``PENDING-HUMAN-VERIFICATION``.
- The 312.305(b)(2) remap (M8) was checked against eCFR by the regulator
  persona review, but a persona is not a qualified human: those rows ship
  ``PENDING-HUMAN-VERIFICATION`` until a qualified human verifies each
  pinpoint against eCFR and flips the row — by editing THIS table with their
  name and date. Nothing else flips a row.
- While any citation a rendered document uses is still pending, the document
  footer carries the ``PENDING_FOOTER`` line (see ea_generators._render).

Render the inventory (from the ``engine`` directory):

    python -m ossicro.citations > ../docs/regulatory/CITATION-INVENTORY.md

Pure stdlib. No I/O at import time.
"""

from __future__ import annotations

from typing import Dict, NamedTuple, Tuple

HUMAN_VERIFIED = "HUMAN-VERIFIED"
PENDING_HUMAN_VERIFICATION = "PENDING-HUMAN-VERIFICATION"

# The one line a rendered document gains while any citation it uses is still
# pending human verification (Overhaul P1 spec item 5).
PENDING_FOOTER = (
    "[PENDING-HUMAN-VERIFICATION] Citation pinpoints marked pending "
    "verification against eCFR — see CITATION-INVENTORY."
)


class Citation(NamedTuple):
    pinpoint: str
    status: str                # HUMAN_VERIFIED | PENDING_HUMAN_VERIFICATION
    verified_by: str = ""      # the qualified human's name — filled by a human
    verified_date: str = ""    # YYYY-MM-DD — filled by the same human
    note: str = ""             # judgment calls the human verifier must see


def _pending(pinpoint: str, note: str = "") -> Citation:
    return Citation(pinpoint, PENDING_HUMAN_VERIFICATION, "", "", note)


# ---------------------------------------------------------------------------
# The table. Keys are content keys (what the citation is FOR), so a pinpoint
# correction is one edit here and every consumer follows.
# ---------------------------------------------------------------------------

CITATIONS: Dict[str, Citation] = {
    # -- 21 CFR 312.305(b)(2): expanded-access treatment-plan content
    #    requirements. M8 remap applied 2026-07-11 (regulator persona map:
    #    every roman-numeral pinpoint was off by one; (b)(2)(i) is the
    #    facts-establishing-availability element, so content starts at (ii)).
    "ea.treatment_plan.rationale": _pending(
        "21 CFR 312.305(b)(2)(ii)",
        "M8 remap: was (b)(2)(i). Rationale for the intended treatment use."),
    "ea.treatment_plan.patient_description": _pending(
        "21 CFR 312.305(b)(2)(iii)",
        "M8 remap: was (b)(2)(ii). Patient description / diagnosis / prior "
        "therapies / coded identifier."),
    "ea.treatment_plan.dosing": _pending(
        "21 CFR 312.305(b)(2)(iv)",
        "M8 remap: was (b)(2)(iii). Method of administration, dose, duration; "
        "treatment-plan summary and composed dosing_plan."),
    "ea.treatment_plan.facility": _pending(
        "21 CFR 312.305(b)(2)(v)",
        "M8 remap: was (b)(2)(iv). Facility description / site.name."),
    "ea.treatment_plan.cmc": _pending(
        "21 CFR 312.305(b)(2)(vi)",
        "M8 remap: was (b)(2)(v). Chemistry, manufacturing, and controls."),
    "ea.treatment_plan.pharmtox": _pending(
        "21 CFR 312.305(b)(2)(vii)",
        "M8 remap: was (b)(2)(vi). Pharmacology and toxicology."),
    "ea.treatment_plan.monitoring": _pending(
        "21 CFR 312.305(b)(2)(viii)",
        "M8 remap: was (b)(2)(vii). JUDGMENT CALL for the human verifier: "
        "monitoring is mapped to (viii) — the treatment plan's clinical "
        "monitoring to evaluate drug effects and minimize risk — NOT to the "
        "(iv) administration-adjacent procedures. Confirm against eCFR."),

    # -- Statutory clocks (HC3: computed, never judged). Each pinpoint is the
    #    clock's authority; the day-count/basis live in ossicro.clocks and the
    #    route registry and are covered by the attestation worksheet.
    "clock.written_3926": _pending(
        "21 CFR 312.310(d)(2)",
        "15 WORKING days: written 3926 after FDA emergency (telephone) "
        "authorization. Anchor: the AUTHORIZATION date."),
    "clock.irb_emergency_notification": _pending(
        "21 CFR 56.104(c)",
        "5 WORKING days: IRB notification after emergency use. Anchor: the "
        "emergency USE, i.e. the FIRST-TREATMENT date — never the FDA "
        "authorization date (M1)."),
    "clock.ind_effective_30_day": _pending(
        "21 CFR 312.40(b)(1)",
        "30 CALENDAR days after FDA receipt: IND effective absent hold or "
        "earlier notification."),
    "clock.ind_annual_report": _pending(
        "21 CFR 312.33",
        "Annual report within 60 CALENDAR days of each anniversary of the "
        "IND-effective date (effective = receipt + 30 per 312.40(b)(1); "
        "Feb-29 effective dates anniversary on Feb 28)."),
    "clock.safety_report_15": _pending(
        "21 CFR 312.32(c)(1)",
        "15 CALENDAR days: IND safety report of a serious and unexpected "
        "suspected adverse reaction, per event."),
    "clock.safety_report_7": _pending(
        "21 CFR 312.32(c)(2)",
        "7 CALENDAR days: fatal/life-threatening unexpected suspected "
        "adverse reaction, from initial receipt, per event."),

    # -- Overhaul P2: pinpoints the new intake-schema fields introduce
    #    (registry facts now; Packages 4-7 render them). From P1 on no new
    #    pinpoint bypasses this table; routes.json cannot call cite(), so a
    #    reconciliation test pins its field citations to these rows.
    "consent.general_requirements": _pending(
        "21 CFR 50.20",
        "General requirements for informed consent — the attestation frame "
        "for consent.timing_attestation."),
    "consent.emergency_exception": _pending(
        "21 CFR 50.23",
        "Exception from the general consent requirements (emergency use); "
        "the documented-exception arm of consent.timing_attestation."),
    "consent.element_injury_compensation": _pending(
        "21 CFR 50.25(a)(6)",
        "Consent element 6: whether compensation and whether medical "
        "treatments are available if injury occurs "
        "(consent.injury_compensation_statement; P6 renders it)."),
    "consent.element_costs": _pending(
        "21 CFR 50.25(b)(3)",
        "Additional-costs consent element (consent.cost_statement; pairs "
        "with the 312.8(d) cost-recovery disclosure)."),
    "charging.expanded_access": _pending(
        "21 CFR 312.8",
        "Charging for investigational drugs under an IND "
        "(submission.cost_recovery_statement; first appearance of 312.8 in "
        "the repo — P4 routes the LOA-request charging line through this "
        "row)."),
    "charging.consent_disclosure": _pending(
        "21 CFR 312.8(d)",
        "Cost-recovery: charging limited to direct costs; the consent cost "
        "statement cross-cites it."),
    # -- Overhaul P6: the EA-profiled informed-consent form's additional
    #    Part-50 elements and its treatment-use framing. HITL: the consent
    #    LANGUAGE itself also carries a document-level
    #    PENDING-HUMAN-VERIFICATION banner (ea_generators.ICF_EA_PENDING_
    #    BANNER) until a qualified, IRB-experienced human reviews it.
    "consent.element_stopping": _pending(
        "21 CFR 50.25(b)(4)",
        "Additional consent element: consequences of a decision to withdraw "
        "and procedures for orderly termination (the EA ICF's stopping-"
        "treatment paragraph; P6 renders it)."),
    "consent.element_new_findings": _pending(
        "21 CFR 50.25(b)(5)",
        "Additional consent element: significant new findings that may "
        "affect willingness to continue (the EA ICF's new-information "
        "paragraph; P6 renders it)."),
    "ea.consent.treatment_framing": _pending(
        "FDA Guidance: Individual Patient Expanded Access Applications - "
        "Form FDA 3926 (treatment-use consent framing)",
        "The EA ICF opens with treatment-use framing (treatment, not a "
        "research study) per FDA's individual-patient expanded-access "
        "guidance, resolving the therapeutic misconception in both "
        "directions. Guidance-based, not a CFR pinpoint: the human "
        "verifier confirms the framing against the current guidance "
        "edition."),
    "ea.end_of_treatment_summary": _pending(
        "21 CFR 312.310(c)(2)",
        "Written summary of the expanded-access use, including adverse "
        "effects, at the conclusion of treatment (treatment.conclusion_date "
        "arms it; P7 renders the obligations row)."),
}


# ---------------------------------------------------------------------------
# Lookup API
# ---------------------------------------------------------------------------

def cite(key: str) -> str:
    """The pinpoint for a content key. KeyError on an unregistered key —
    fail loud, never invent a citation (HC2)."""
    return CITATIONS[key].pinpoint


def cite_range(key_from: str, key_to: str) -> str:
    """Render two adjacent sub-element pinpoints as one range, e.g.
    cite_range('ea.treatment_plan.cmc', 'ea.treatment_plan.pharmtox') ->
    '21 CFR 312.305(b)(2)(vi)-(vii)'."""
    first = cite(key_from)
    last = cite(key_to)
    return "%s-(%s" % (first, last.rsplit("(", 1)[1])


def pending_pinpoints() -> Tuple[str, ...]:
    """Every distinct pinpoint whose table row is still pending human
    verification, sorted for determinism."""
    return tuple(sorted({c.pinpoint for c in CITATIONS.values()
                         if c.status == PENDING_HUMAN_VERIFICATION}))


def uses_pending(*texts: str) -> bool:
    """True when any pending pinpoint appears in any of the given texts
    (a document's rendered body and/or its provenance citation strings)."""
    hay = "\n".join(t for t in texts if t)
    return any(p in hay for p in pending_pinpoints())


# ---------------------------------------------------------------------------
# Inventory rendering — docs/regulatory/CITATION-INVENTORY.md
# ---------------------------------------------------------------------------

def render_inventory() -> str:
    """The citation inventory as Markdown (the committed doc is this output;
    a test keeps the two in sync)."""
    lines = [
        "# OSSICRO Citation Inventory",
        "",
        "**GENERATED** from the single-source table "
        "`engine/ossicro/citations.py` — regenerate with "
        "`python -m ossicro.citations > ../docs/regulatory/"
        "CITATION-INVENTORY.md` (from `engine/`). Do not edit this file by "
        "hand; edit the table.",
        "",
        "**Human-verification rule (HITL).** A row flips from "
        "`PENDING-HUMAN-VERIFICATION` to `HUMAN-VERIFIED` ONLY when a "
        "qualified human verifies the pinpoint against eCFR and records "
        "their name and date in the table in `citations.py`. AI/persona "
        "review is not a substitute. While any row a document uses is "
        "pending, the rendered document carries the pending-footer line.",
        "",
        "| Key | Pinpoint | Status | Verified by | Verified date | Note |",
        "|---|---|---|---|---|---|",
    ]
    for key in sorted(CITATIONS):
        c = CITATIONS[key]
        lines.append("| `%s` | %s | %s | %s | %s | %s |" % (
            key, c.pinpoint, c.status, c.verified_by or "—",
            c.verified_date or "—", c.note or "—"))
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    sys.stdout.write(render_inventory())
