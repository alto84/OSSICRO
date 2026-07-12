"""EA GENERATE pass: generators for the Route-3926 expanded-access document set.

Same discipline as ossicro.generate: ``{{field}}`` substitution over a template
string; every filled field emits a ProvenanceRecord (span -> source datum ->
citation); a field whose source datum is missing renders as an explicit
``[[MISSING: field]]`` marker and is omitted from ``Document.fields`` so the
CHECK pass turns it into a red ledger item with the exact resolving question.

Nothing here performs a non-delegable act (Constitution HC1): every output is a
DRAFT for a qualified human. The physician signs the 3926 and cover letter
(``submission-to-fda`` gate), obtains consent (``informed-consent``), and routes
IRB concurrence (``irb-approval``); the manufacturer signs the LOA. OSSICRO
drafts and records; it never signs, consents, approves, or files.

Statutory clocks are computed here deterministically (HC3): working-day and
calendar-day calendars are distinct, and the trigger dates are human-entered.
"""

from __future__ import annotations

import datetime
import re
from typing import Callable, Dict, List, Optional, Tuple

from . import citations
from . import generate as builtin_generate
from . import pdf_3926 as _form3926
from .citations import cite as _C
from .clocks import (
    add_working_days,
    federal_holidays,
    ind_30_day_deadline,
    ind_annual_report_deadline,
    irb_emergency_notification_deadline,
    working_days_between,
    written_3926_deadline,
)
from .models import Document, ProvenanceRecord, Study

_PLACEHOLDER = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
MISSING_MARKER = "[[MISSING: %s]]"


class _Optional(str):
    """A literal whose value is legitimately allowed to be empty — it renders
    as-is (empty = nothing) instead of the MISSING marker. Used for computed
    connective text like the credential suffix, which is *absent*, not *missing*
    (distinct from an unanswered attestation, which must render MISSING)."""


# ---------------------------------------------------------------------------
# Study construction from flat, dotted intake keys
# ---------------------------------------------------------------------------

def unflatten(flat: Dict[str, object]) -> Dict[str, object]:
    """Turn {'patient.coded_id': 'X'} into {'patient': {'coded_id': 'X'}}."""
    root: Dict[str, object] = {}
    for key, value in flat.items():
        parts = key.split(".")
        node = root
        for part in parts[:-1]:
            nxt = node.get(part)
            if not isinstance(nxt, dict):
                nxt = {}
                node[part] = nxt
            node = nxt
        node[parts[-1]] = value
    return root


def build_study(intake_flat: Dict[str, object], route: Dict[str, object]) -> Study:
    """Assemble a Study record from flat intake and the selected route.

    The route's ordered document list becomes ``required_documents`` so the
    completeness ledger scopes to exactly this submission. A derived title and
    the (optional) IND number are set for cross-document consistency; nothing is
    invented — absent facts stay absent.
    """
    raw = unflatten(intake_flat)
    drug_name = ((raw.get("drug") or {}).get("name") if isinstance(raw.get("drug"), dict) else "") or "the investigational drug"
    raw.setdefault("title", "Individual-patient expanded access treatment with %s" % drug_name)
    submission = raw.get("submission") if isinstance(raw.get("submission"), dict) else {}
    if submission.get("ind_number"):
        raw["ind_number"] = submission["ind_number"]
    # The consent form (built-in ICF) reads top-level protocol identifiers. In
    # single-patient EA there is no trial protocol; the treatment-plan identifier
    # (if the physician supplied one) stands in. Absent, the ICF stays honestly
    # incomplete (red) rather than carrying an invented number.
    treatment = raw.get("treatment") if isinstance(raw.get("treatment"), dict) else {}
    if treatment.get("plan_id"):
        raw.setdefault("protocol_number", treatment["plan_id"])
    if treatment.get("plan_version"):
        raw.setdefault("protocol_version", treatment["plan_version"])
    raw["required_documents"] = list(route.get("documents", []))
    return Study.from_dict(raw)


# ---------------------------------------------------------------------------
# Deterministic clock engine (HC3): working-day vs calendar-day calendars.
#
# The calendar arithmetic itself is the canonical engine in ossicro.clocks
# (weekend + observed-federal-holiday rules, verified against a fixed table).
# This module owns only the intake-facing plumbing: parsing a human-entered
# trigger string and mapping the route's working/calendar selector onto the
# canonical functions. ``add_working_days``, ``federal_holidays``,
# ``written_3926_deadline``, ``irb_emergency_notification_deadline``,
# ``ind_30_day_deadline`` and ``ind_annual_report_deadline`` are re-exported
# from clocks so callers (and tests) reach one source of truth. The two
# emergency deadlines are SEPARATE single-anchor functions (M1): the written
# 3926 runs from the FDA authorization, the IRB notification from the first
# treatment — each takes only its own keyword-named anchor.
# ---------------------------------------------------------------------------

__all__ = [
    "add_working_days",
    "federal_holidays",
    "written_3926_deadline",
    "irb_emergency_notification_deadline",
    "ind_30_day_deadline",
    "ind_annual_report_deadline",
    "TriggerDateError",
    "parse_trigger_date",
    "derive_as_of",
    "compute_deadline",
    "compute_clocks",
    "build_study",
    "unflatten",
    "generate_route_documents",
    "gen_icf_ea",
    "ICF_EA_FIELD_SOURCES",
    "ICF_EA_PENDING_BANNER",
]


class TriggerDateError(ValueError):
    """A physician-entered trigger date is present but unparseable.

    Raised (never swallowed) so the bad entry surfaces to the user as an
    error; a garbled date must not be silently treated as absent (HC2).
    """

    def __init__(self, field_id: str, value: object):
        self.field_id = field_id
        self.value = value
        super().__init__(
            "Unparseable date %r in intake field '%s' — enter it as YYYY-MM-DD."
            % (value, field_id)
        )


def parse_trigger_date(text: Optional[str], field_id: str) -> Optional[datetime.date]:
    """Parse a human-entered trigger date.

    Absent (None/blank) returns None — an unarmed clock, honestly pending.
    Present but unparseable raises TriggerDateError — an error to surface,
    never a silent absence.
    """
    if text is None or not str(text).strip():
        return None
    head = str(text).strip()[:10]
    try:
        return datetime.datetime.strptime(head, "%Y-%m-%d").date()
    except ValueError:
        raise TriggerDateError(field_id, text)


# Intake fields, in priority order, that can anchor document dates (the
# ``as_of`` the generators stamp on cover/request dates). All are
# physician-entered facts; the engine NEVER anchors on the wall clock.
# ``submission.date`` (M5, Overhaul P2) is a live routes.json intake field —
# "Preparation / planned submission date" — so the primary anchor is now
# reachable from the intake form; it also backstops the 30-day IND clock
# trigger below. Absent every field here, dated spans render as explicit
# MISSING markers.
_AS_OF_FIELDS = (
    "submission.date",
    "submission.emergency_auth_datetime",
    "submission.first_treatment_date",
    "submission.fda_receipt_date",
)


def derive_as_of(study: Study) -> Optional[datetime.date]:
    """The document anchor date derived from physician-entered trigger dates.

    Returns the first present trigger date in priority order, or None when the
    intake carries no date at all — in which case dated spans render as
    explicit MISSING markers rather than a fabricated 'today'.
    """
    for field_id in _AS_OF_FIELDS:
        value = study.resolve(field_id)
        if value is not None:
            return parse_trigger_date(value, field_id)
    return None


def compute_deadline(trigger: Optional[str], days: int, calendar: str,
                     field_id: str = "trigger") -> Optional[str]:
    """Return the ISO deadline for a trigger date, or None if no trigger given.

    ``working`` days route through the canonical ossicro.clocks engine (weekends
    + observed federal holidays); ``calendar`` days are a plain span. An
    unparseable trigger raises TriggerDateError.
    """
    start = parse_trigger_date(trigger, field_id)
    if start is None:
        return None
    if calendar == "working":
        return add_working_days(start, days).isoformat()
    return (start + datetime.timedelta(days=days)).isoformat()


def compute_clocks(study: Study, route: Dict[str, object],
                   as_of: Optional[datetime.date] = None) -> List[Dict[str, object]]:
    """Compute every clock the route arms. Trigger dates are human-entered.

    A clock with no trigger date entered is UNARMED: ``armed=False``, a null
    deadline, and a ``resolving_question`` naming the trigger to enter —
    honestly pending, never guessed from the wall clock. An unparseable
    trigger raises TriggerDateError. ``days_remaining`` is computed only when
    both a deadline and an ``as_of`` anchor exist (working-day clocks count
    working days; calendar clocks count calendar days).
    """
    out: List[Dict[str, object]] = []
    for clock in route.get("clocks", []):
        trigger_field = clock["trigger_field"]
        trigger_value = study.resolve(trigger_field)
        effective_field = trigger_field
        # The 30-day IND clock defaults its trigger to the submission date —
        # a recorded fact, never the wall clock.
        if trigger_value is None and clock["id"] == "ind-effective-30-day":
            trigger_value = study.resolve("submission.date")
            effective_field = "submission.date"
        deadline = compute_deadline(trigger_value, clock["days"], clock["calendar"],
                                    field_id=effective_field)
        armed = deadline is not None
        resolving_question = None if armed else (
            "Enter the trigger date (intake field '%s') to arm the '%s' clock (%s)."
            % (trigger_field, clock["label"], clock["basis"])
        )
        days_remaining = None
        if armed and as_of is not None:
            due = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            if clock["calendar"] == "working":
                days_remaining = working_days_between(as_of, due)
            else:
                days_remaining = (due - as_of).days
        out.append({
            "id": clock["id"],
            "label": clock["label"],
            "basis": clock["basis"],
            "owner": clock["owner"],
            "calendar": clock["calendar"],
            "days": clock["days"],
            "trigger_field": trigger_field,
            "trigger_value": trigger_value,
            "deadline": deadline,
            "armed": armed,
            "days_remaining": days_remaining,
            "resolving_question": resolving_question,
            "note": clock.get("note", ""),
        })
    return out


def _anchor_literal(as_of: Optional[datetime.date], citation: str) -> Tuple[Optional[str], str, str]:
    """A dated-span literal anchored to the physician-entered ``as_of`` date.

    When no anchor exists the value is None, so the span renders as an explicit
    ``[[MISSING: ...]]`` marker — an honest gap, never a fabricated 'today'.
    """
    value = as_of.isoformat() if as_of is not None else None
    return (value, citation, "physician-entered anchor date (as_of)")


# ---------------------------------------------------------------------------
# Generic renderer
# ---------------------------------------------------------------------------

def _render(
    doc_id: str,
    template: str,
    sources: Dict[str, Tuple[str, str]],
    doc_registry: Dict[str, dict],
    study: Study,
    literals: Optional[Dict[str, Tuple[str, str, str]]] = None,
    extra_fields: Optional[Dict[str, Tuple[str, str]]] = None,
) -> Document:
    """Instantiate ``template`` for ``doc_id`` from ``study``.

    ``sources``      placeholder -> (study-record path, citation)
    ``literals``     placeholder -> (computed value, citation, source-label) — a
                     value produced by the engine (e.g. a computed clock date),
                     provenance-stamped to its computation, never to invented fact
    ``extra_fields`` registry-required field -> (path, citation) to guarantee the
                     field lands in Document.fields even when it is not a template
                     placeholder (keeps the completeness ledger honest)
    """
    literals = literals or {}
    entry = doc_registry.get(doc_id, {})
    fields: Dict[str, str] = {}
    provenance: List[ProvenanceRecord] = []

    def substitute(match: "re.Match[str]") -> str:
        name = match.group(1)
        if name in literals:
            value, citation, source_label = literals[name]
            if value is None or (str(value).strip() == "" and not isinstance(value, _Optional)):
                return MISSING_MARKER % name
            value = str(value)
            if name not in fields:
                fields[name] = value
                provenance.append(ProvenanceRecord(span=name, source=source_label, citation=citation))
            return value
        if name in sources:
            path, citation = sources[name]
            value = study.resolve(path)
            if value is None:
                return MISSING_MARKER % name
            if name not in fields:
                fields[name] = value
                provenance.append(
                    ProvenanceRecord(span=name, source="%s = %r" % (path, value), citation=citation)
                )
            return value
        return MISSING_MARKER % name

    rendered = _PLACEHOLDER.sub(substitute, template)

    for field_name, (path, citation) in (extra_fields or {}).items():
        if field_name in fields:
            continue
        value = study.resolve(path)
        if value is not None:
            fields[field_name] = value
            provenance.append(
                ProvenanceRecord(span=field_name, source="%s = %r" % (path, value), citation=citation)
            )

    # HITL (Overhaul P1 spec item 5): while any citation this document uses —
    # in its rendered body or its provenance — is still PENDING-HUMAN-
    # VERIFICATION in the single-source table, the artifact itself says so.
    # The line disappears only when a qualified human flips the rows in
    # ossicro.citations; it is never removed by code.
    if citations.uses_pending(rendered, *(p.citation for p in provenance)):
        rendered += "\n" + citations.PENDING_FOOTER + "\n"

    return Document(
        doc_id=doc_id,
        title=entry.get("title", doc_id),
        state="draft",
        fields=fields,
        provenance=provenance,
        rendered=rendered,
        gate_id=entry.get("gate"),
    )


# ---------------------------------------------------------------------------
# Cover letter (EA-profiled)  —  spec §2
# ---------------------------------------------------------------------------

_COVER_TEMPLATE = """\
EXPANDED ACCESS COVER LETTER                                          [DRAFT]
Authority: 21 CFR 312.23(a)(1); 21 CFR 312.310

{{cover_date}}

Food and Drug Administration
{{fda_division}}

Re: Individual Patient Expanded Access IND — {{patient_initials_coded}} — {{drug_name}}
    {{submission_kind}}

Dear Sir or Madam:

1. STATEMENT OF REQUEST. I, {{investigator_name}}{{degrees_suffix}}, a licensed
   physician, request authorization under 21 CFR 312.310 to treat one patient
   ({{patient_initials_coded}}) who has a serious or immediately life-threatening
   condition for which there is no comparable or satisfactory alternative
   therapy. Diagnosis: {{diagnosis}}

2. §312.305(a) CRITERIA.
   (a) Serious/life-threatening + no alternative: {{no_alternative_basis}}
   (b) Potential benefit justifies potential risk: {{benefit_risk}}
   (c) Use will not interfere with clinical investigations: {{non_interference}}

3. §312.310(a) DETERMINATION. I have determined that the probable risk to this
   patient from {{drug_name}} is not greater than the probable risk from the
   disease or condition: {{risk_determination}}

4. LETTER OF AUTHORIZATION. The manufacturer, {{manufacturer_name}}, has been
   asked to authorize FDA to cross-reference {{ind_dmf_reference}} for chemistry,
   manufacturing, pharmacology, and toxicology information (21 CFR 312.23(b)).

5. IND EFFECTIVE / CLOCKS.
   {{clock_statement}}

6. ENCLOSURES. Form FDA 3926; expanded-access treatment plan; manufacturer
   Letter of Authorization (enclosed upon receipt from the manufacturer);
   IRB concurrence evidence; informed consent form.

7. CONTACT. {{investigator_name}}, {{investigator_phone}}, {{investigator_email}}.
   IRB of record: {{irb_name}}.

Respectfully submitted,

______________________________________________  Date: __________
{{investigator_name}}{{degrees_suffix}}
   [NON-DELEGABLE HUMAN ACT — gate: submission-to-fda. OSSICRO drafts this
    letter; only the sponsor-investigator signs and files it. 21 CFR 312.20,
    312.23, 312.40.]
"""


def _is_emergency(study: Study) -> bool:
    """The one emergency-flag parse (Overhaul P4): the cover letter, the IRB
    request, and the LOA-request urgency literal all read submission.emergency
    through this helper — one computation, three consumers."""
    return str(study.resolve("submission.emergency") or "").strip().lower() in ("true", "1", "yes")


def _degrees_suffix(name: Optional[str], degrees: Optional[str]) -> str:
    """Return ", {degrees}" — unless the name already carries the credential.

    ``investigator.name`` comes from ``Practitioner.name`` including its suffix
    (e.g. "Jordan A. Rivera, MD"), while ``investigator.degrees`` is a separate
    field ("MD"). Appending unconditionally produced "…Rivera, MD, MD" in the
    cover letter, signature block, and LOA request (UI-QA F1). Dedupe here.
    """
    if not degrees:
        return _Optional("")
    n = (name or "").lower().replace(".", "").rstrip()
    d = degrees.strip().lower().replace(".", "")
    if d and n.endswith(d):
        return _Optional("")
    return _Optional(", " + degrees)


def gen_cover_letter(study: Study, doc_registry: Dict[str, dict],
                     as_of: Optional[datetime.date] = None) -> Document:
    degrees = study.resolve("investigator.degrees")
    emergency = _is_emergency(study)
    kind_bits = []
    kind_bits.append("EMERGENCY REQUEST" if emergency else "Non-emergency request")
    initial = (study.resolve("submission.initial_or_followup") or "initial").strip().lower()
    ind_no = study.resolve("submission.ind_number")
    if initial == "followup":
        kind_bits.append("Follow-up submission" + (" to IND %s" % ind_no if ind_no else ""))
    else:
        kind_bits.append("Initial application")
    submission_kind = " | ".join(kind_bits)

    if emergency:
        auth = study.resolve("submission.emergency_auth_datetime")
        auth_date = parse_trigger_date(auth, "submission.emergency_auth_datetime")
        if auth_date is not None:
            # The 15-working-day written-3926 clock runs from the FDA
            # authorization (single-anchor canonical helper, M1).
            written = written_3926_deadline(authorization_date=auth_date)
            clock_statement = (
                "This written submission is filed within 15 WORKING DAYS of the FDA "
                "telephone authorization dated %s; that deadline is %s (%s)."
                % (auth, written.due.isoformat(), _C("clock.written_3926"))
            )
        else:
            clock_statement = (
                "EMERGENCY: enter the FDA telephone-authorization date so OSSICRO can "
                "compute the 15-working-day written-3926 deadline (%s)."
                % _C("clock.written_3926")
            )
        clock_cite = _C("clock.written_3926")
    else:
        receipt = study.resolve("submission.fda_receipt_date")
        receipt_date = parse_trigger_date(receipt, "submission.fda_receipt_date")
        if receipt_date is not None:
            deadline = ind_30_day_deadline(receipt_date).due.isoformat()
            clock_statement = (
                "For a non-emergency request, treatment may not begin until FDA notifies "
                "the physician it may proceed, or — absent notification — 30 CALENDAR DAYS "
                "after FDA receipt (%s), i.e. %s (%s)."
                % (receipt, deadline, _C("clock.ind_effective_30_day"))
            )
        else:
            clock_statement = (
                "Enter the FDA receipt date (submission.fda_receipt_date) so OSSICRO can "
                "compute the 30-CALENDAR-DAY IND-effective date; treatment may not begin "
                "until FDA notifies the physician it may proceed, or — absent "
                "notification — 30 calendar days after FDA receipt (%s)."
                % _C("clock.ind_effective_30_day")
            )
        clock_cite = _C("clock.ind_effective_30_day")

    literals = {
        "cover_date": _anchor_literal(as_of, "21 CFR 312.23(a)(1)"),
        "submission_kind": (submission_kind, "Form FDA 3926", "computed from submission.* intake"),
        "degrees_suffix": (_degrees_suffix(study.resolve("investigator.name"), degrees),
                           "21 CFR 312.310(a)",
                           "computed from investigator.degrees; omitted if the name already carries the credential"),
        "clock_statement": (clock_statement, clock_cite, "computed clock (HC3)"),
    }
    sources = {
        "fda_division": ("submission.fda_division", "21 CFR 312.310(d)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.310"),
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "investigator_name": ("investigator.name", "21 CFR 312.310(a)"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
        "no_alternative_basis": ("patient.no_alternative_basis", "21 CFR 312.305(a)(1)"),
        "benefit_risk": ("treatment.benefit_risk", "21 CFR 312.305(a)(2)"),
        "non_interference": ("treatment.non_interference", "21 CFR 312.305(a)(3)"),
        "risk_determination": ("investigator.risk_determination", "21 CFR 312.310(a)"),
        "manufacturer_name": ("manufacturer.name", "FDCA 561A"),
        "ind_dmf_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "investigator_phone": ("investigator.phone", "Form FDA 3926"),
        "investigator_email": ("investigator.email", "Form FDA 3926"),
        "irb_name": ("irb.name", "21 CFR 56.104/.105"),
    }
    extra = {"fda_division": ("submission.fda_division", "21 CFR 312.310(d)")}
    return _render("expanded-access-cover-letter", _COVER_TEMPLATE, sources,
                   doc_registry, study, literals=literals, extra_fields=extra)


# ---------------------------------------------------------------------------
# Form FDA 3926  —  spec §1.1 item 2, §6 waivers
#
# P8: the section order/numbering below is CONSUMED from the one item map
# (pdf_3926.FORM_3926_ITEMS) — the same table the PDF layout and the FDF
# field map derive from, so the renders cannot disagree again. The heading
# is softened to a draft layout and the artifact carries the
# PENDING-HUMAN-VERIFICATION numbering marker until a qualified human
# initials pdf_3926.FORM_3926_MAP_VERIFIED_BY.
# ---------------------------------------------------------------------------

_3926_HEADINGS = {item.number: "%s. %s" % (item.number, item.label)
                  for item in _form3926.FORM_3926_ITEMS}

_FORM_3926_TEMPLATE = """\
FORM FDA 3926 (DRAFT LAYOUT) — INDIVIDUAL PATIENT EXPANDED ACCESS IND [DRAFT]
Authority: 21 CFR 312.310; Form FDA 3926 (OMB 0910-0814)
{{pending_numbering_note}}

 %(h1)s: {{submission_date}}
 %(h2)s: {{submission_kind}}   (IND #: {{ind_number}})
 %(h3)s
    Patient identifier (coded — no direct identifiers): {{patient_initials_coded}}
    Age: {{patient_age}}   Sex: {{patient_sex}}
    Diagnosis / condition: {{diagnosis}}
    Prior therapies and outcomes: {{prior_therapies}}
    Clinical rationale (seriousness; no satisfactory alternative; benefit
    justifies risk — 21 CFR 312.305(a)): {{clinical_rationale}}
 %(h4)s
    Investigational drug: {{drug_name}}     Manufacturer / source: {{manufacturer_name}}
    Treatment plan summary (full plan attached): {{treatment_plan_summary}}
    Dose: {{dose}}   Route: {{route}}   Planned duration: {{duration}}
    Monitoring: {{monitoring_plan}}
 %(h5)s
    LOA cross-references application: {{loa_reference}}
 %(h6)s
    {{physician_name}}{{degrees_suffix}}; license {{license_number}} ({{license_state}}).
    §312.310(a) determination (risk drug <= risk disease): {{risk_determination}}
 %(h7)s
    {{physician_name}}{{degrees_suffix}}
    {{physician_address}}
    {{physician_phone}}   {{physician_email}}
 %(h8)s
    IRB of record: {{irb_name}}
 %(h9)s
    [UNRESOLVED — the local Form-3926 instructions/guidance does not
     enumerate this item; the human pass transcribes it from the official
     fillable form.]
%(h10)s
    10.a WAIVER (§312.10 — waive additional Part 312 / Forms 1571 & 1572
       requirements): {{waiver_10a}}
    10.b WAIVER (§56.105 — IRB chairperson concurrence in lieu of convened
       board): {{waiver_10b}}
    [Fields 10.a / 10.b are physician attestations; OSSICRO never defaults or
     auto-checks them.]
%(h11)s
    SIGNATURE: ____________________________________  DATE: __________
   [NON-DELEGABLE HUMAN ACT — gate: submission-to-fda. Software cannot be a
    sponsor (21 CFR 312.52) and cannot execute this signature or file the form.]
""" % {"h%s" % item.number: _3926_HEADINGS[item.number]
       for item in _form3926.FORM_3926_ITEMS}


def _bool_label(study: Study, path: str) -> str:
    raw = study.resolve(path)
    if raw is None:
        return ""  # unanswered -> renders MISSING, honestly
    return "CHECKED (physician-attested)" if str(raw).strip().lower() in ("true", "1", "yes") else "not checked"


def gen_form_3926(study: Study, doc_registry: Dict[str, dict],
                  as_of: Optional[datetime.date] = None) -> Document:
    degrees = study.resolve("investigator.degrees")
    initial = (study.resolve("submission.initial_or_followup") or "initial").strip().lower()
    emergency = _is_emergency(study)
    kind = ("(b) Initial — EMERGENCY use (21 CFR 312.310(d))" if emergency
            else "(a) Initial application") if initial != "followup" else "(c) Follow-up submission"
    # Compose the treatment-plan summary and clinical rationale required fields.
    # Item-number citations route through pdf_3926.item_citation — the one
    # item map — and stay honest about its verification state (P8).
    _FI = _form3926.item_citation
    literals = {
        "submission_date": _anchor_literal(as_of, _FI("1")),
        "submission_kind": (kind, "%s; 21 CFR 312.310(d)" % _FI("2"), "computed from submission.* intake"),
        "degrees_suffix": (_degrees_suffix(study.resolve("investigator.name"), degrees),
                           "21 CFR 312.310(a)",
                           "computed from investigator.degrees; omitted if the name already carries the credential"),
        "waiver_10a": (_bool_label(study, "waiver_10a"), "21 CFR 312.10", "physician attestation: waiver_10a"),
        "waiver_10b": (_bool_label(study, "waiver_10b"), "21 CFR 56.105", "physician attestation: waiver_10b"),
        # P8 HITL marker: present until a qualified human initials the item
        # map (pdf_3926.FORM_3926_MAP_VERIFIED_BY) — never removed by code.
        "pending_numbering_note": (
            _Optional(_form3926.pending_item_numbering_note()),
            "Form FDA 3926 (OMB 0910-0814)",
            "P8 item-map verification state (pdf_3926.FORM_3926_ITEMS)"),
    }
    sources = {
        "ind_number": ("submission.ind_number", _FI("2")),
        "patient_initials_coded": ("patient.coded_id", "%s; 21 CFR 312.310" % _FI("3")),
        "patient_age": ("patient.age", _FI("3")),
        "patient_sex": ("patient.sex", _FI("3")),
        "diagnosis": ("patient.diagnosis", "%s; 21 CFR 312.305(a)(1)" % _FI("3")),
        "prior_therapies": ("patient.prior_therapies", "21 CFR 312.310(a)"),
        "clinical_rationale": ("request.clinical_rationale", "21 CFR 312.305(a); 312.310(a)"),
        "drug_name": ("drug.name", _FI("4")),
        "manufacturer_name": ("manufacturer.name", _FI("4")),
        "treatment_plan_summary": ("treatment.benefit_risk", _C("ea.treatment_plan.dosing")),
        "dose": ("drug.dose", _C("ea.treatment_plan.dosing")),
        "route": ("drug.route", _C("ea.treatment_plan.dosing")),
        "duration": ("drug.duration", _C("ea.treatment_plan.dosing")),
        "monitoring_plan": ("treatment.monitoring_plan", _C("ea.treatment_plan.monitoring")),
        "loa_reference": ("manufacturer.ind_dmf_reference", "%s; 21 CFR 312.23(b)" % _FI("5")),
        "physician_name": ("investigator.name", "%s; 21 CFR 312.310(a)" % _FI("7")),
        "license_number": ("investigator.license_number", "%s; 21 CFR 312.310(a)" % _FI("6")),
        "license_state": ("investigator.license_state", "%s; 21 CFR 312.310(a)" % _FI("6")),
        "risk_determination": ("investigator.risk_determination", "%s; 21 CFR 312.310(a)" % _FI("6")),
        "irb_name": ("irb.name", "%s; 21 CFR Part 56" % _FI("8")),
        "physician_address": ("investigator.address", _FI("7")),
        "physician_phone": ("investigator.phone", _FI("7")),
        "physician_email": ("investigator.email", _FI("7")),
    }
    return _render("form-fda-3926-individual-patient-expanded-access", _FORM_3926_TEMPLATE,
                   sources, doc_registry, study, literals=literals)


# ---------------------------------------------------------------------------
# Expanded-access treatment plan  —  spec §1.1 item 4
# ---------------------------------------------------------------------------

_TREATMENT_PLAN_TEMPLATE = """\
EXPANDED ACCESS TREATMENT PLAN                                       [DRAFT]
Authority: 21 CFR 312.305(b)

Drug: {{drug_name}} | Physician (sponsor-investigator): {{physician_name}}
LOA cross-reference: {{loa_reference}}

1. RATIONALE FOR TREATMENT USE — %(cite_rationale)s
   {{treatment_rationale}}

2. PATIENT DESCRIPTION AND SELECTION — %(cite_patient)s
   Coded patient: {{patient_initials_coded}}   Diagnosis: {{diagnosis}}
   Prior therapies and responses: {{prior_therapies}}
   No comparable/satisfactory alternative — basis: {{no_alternative_basis}}

3. METHOD OF ADMINISTRATION, DOSE, AND DURATION — %(cite_dosing)s
   {{dosing_plan}}
   Route/method: {{route}}   Planned duration: {{duration}}

4. FACILITY AND PERSONNEL — %(cite_facility)s
   Treatment facility: {{facility}}

5. CMC; PHARMACOLOGY/TOXICOLOGY — %(cite_cmc_pharmtox)s
   Incorporated by reference to {{loa_reference}} per the attached LOA
   (21 CFR 312.23(b)); the physician does not author CMC/nonclinical content.

6. MONITORING PLAN — %(cite_monitoring)s
   {{monitoring_plan}}

7. SAFETY REPORTING — 21 CFR 312.305(c), 312.310(c), 312.32
   The sponsor-investigator will report serious, unexpected, suspected adverse
   reactions to FDA per 21 CFR 312.32 and provide the summary/annual report per
   21 CFR 312.310(c)(2). Causality/expectedness is the medical monitor's
   non-delegable judgment (gate: sae-causality).

Treating physician (sponsor-investigator): {{physician_name}}
Signature: ______________________________  Date: __________
""" % {
    # M8 remap ([PT-2]): every 312.305(b)(2) pinpoint is looked up from the
    # single-source table — the roman numerals appear ONLY in citations.py.
    "cite_rationale": _C("ea.treatment_plan.rationale"),
    "cite_patient": _C("ea.treatment_plan.patient_description"),
    "cite_dosing": _C("ea.treatment_plan.dosing"),
    "cite_facility": _C("ea.treatment_plan.facility"),
    "cite_cmc_pharmtox": citations.cite_range("ea.treatment_plan.cmc",
                                              "ea.treatment_plan.pharmtox"),
    "cite_monitoring": _C("ea.treatment_plan.monitoring"),
}


def gen_treatment_plan(study: Study, doc_registry: Dict[str, dict],
                       as_of: Optional[datetime.date] = None) -> Document:
    dose = study.resolve("drug.dose")
    route = study.resolve("drug.route")
    duration = study.resolve("drug.duration")
    dosing_bits = [b for b in [dose and ("Dose: " + dose), route and ("Route: " + route),
                               duration and ("Duration: " + duration)] if b]
    literals = {}
    if dosing_bits:
        literals["dosing_plan"] = ("; ".join(dosing_bits), _C("ea.treatment_plan.dosing"),
                                   "composed from drug.dose/route/duration")
    sources = {
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "physician_name": ("investigator.name", "21 CFR 312.305(c)"),
        "loa_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "treatment_rationale": ("request.clinical_rationale",
                                "%s; 312.305(a)" % _C("ea.treatment_plan.rationale")),
        "patient_initials_coded": ("patient.coded_id", _C("ea.treatment_plan.patient_description")),
        "diagnosis": ("patient.diagnosis", _C("ea.treatment_plan.patient_description")),
        "prior_therapies": ("patient.prior_therapies", _C("ea.treatment_plan.patient_description")),
        "no_alternative_basis": ("patient.no_alternative_basis", "21 CFR 312.305(a)(1); 312.310(a)(2)"),
        "route": ("drug.route", _C("ea.treatment_plan.dosing")),
        "duration": ("drug.duration", _C("ea.treatment_plan.dosing")),
        "facility": ("site.name", _C("ea.treatment_plan.facility")),
        "monitoring_plan": ("treatment.monitoring_plan", _C("ea.treatment_plan.monitoring")),
    }
    return _render("expanded-access-treatment-plan", _TREATMENT_PLAN_TEMPLATE, sources,
                   doc_registry, study, literals=literals)


# ---------------------------------------------------------------------------
# Manufacturer Letter of Authorization (drafted for the manufacturer's review)
# spec §4.1
# ---------------------------------------------------------------------------

_LOA_TEMPLATE = """\
MANUFACTURER LETTER OF AUTHORIZATION (LOA)                           [DRAFT]
Authority: 21 CFR 312.23(b); FDCA 561A
[Draft for the manufacturer's review — issued on {{manufacturer_name}}
 letterhead and signed by an official authorized to bind the company. OSSICRO
 drafts; the physician cannot sign on the manufacturer's behalf. Terms only
 the manufacturer can supply render as explicit MISSING markers — they are
 honestly absent until the manufacturer supplies them.]

[LETTERHEAD]
{{manufacturer_name}}
{{manufacturer_address}}

{{loa_date}}

Food and Drug Administration
{{fda_division}}

Re: Letter of Authorization — Right of Reference to {{drug_master_file_reference}}
    for {{drug_name}}

Dear Sir or Madam:

Pursuant to 21 CFR 312.23(b), {{manufacturer_name}} hereby authorizes the Food
and Drug Administration to reference application {{drug_master_file_reference}}
held by {{manufacturer_name}}, on behalf of the authorized party below, solely
in support of the individual-patient expanded access use described (21 CFR
312.310) for the treatment of one patient with {{diagnosis}}.

  Referenced application(s): {{drug_master_file_reference}}
  Drug product: {{drug_name}}
  Sections authorized: chemistry/manufacturing/controls and pharmacology/toxicology
  Sections expressly excluded (manufacturer to state, or "none"):
    {{sections_expressly_excluded}}

Authorized party (holder of the right of reference):
  {{authorized_party}}
  {{authorized_party_address}}

This authorization is effective as of {{loa_effective_date}} and remains in
effect until {{loa_expiration_or_revocation_terms}}, unless earlier revoked by
written notice to FDA and the authorized party.

Sincerely,

______________________________________________
{{loa_signatory}}
Authorized official, {{manufacturer_name}}
   [EXTERNAL-PARTY ACT — the manufacturer signs this LOA. OSSICRO records the
    returned LOA as a fact (manufacturer.loa_received_date / loa_signatory);
    it never signs or supplies (FDCA 561A).]
"""


def gen_loa(study: Study, doc_registry: Dict[str, dict],
            as_of: Optional[datetime.date] = None) -> Document:
    literals = {
        "loa_date": _anchor_literal(as_of, "21 CFR 312.23(b)"),
    }
    sources = {
        "manufacturer_name": ("manufacturer.name", "21 CFR 312.23(b)"),
        "manufacturer_address": ("manufacturer.address", "21 CFR 312.23(b)"),
        "fda_division": ("submission.fda_division", "21 CFR 312.23(b)"),
        "drug_master_file_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "drug_name": ("drug.name", "21 CFR 312.23(b)"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
        "authorized_party": ("investigator.name", "21 CFR 312.23(b)"),
        "authorized_party_address": ("investigator.address", "21 CFR 312.23(b)"),
        # m4: terms only the manufacturer can supply. The exclusion and
        # effective/expiration terms have NO intake field by design — they
        # render as explicit MISSING markers in the draft (never invented).
        # The signatory line fills only once the received, signed LOA is
        # recorded (manufacturer.loa_signatory); until then it too is MISSING.
        "sections_expressly_excluded": ("manufacturer.loa_sections_excluded", "21 CFR 312.23(b)"),
        "loa_effective_date": ("manufacturer.loa_effective_date", "21 CFR 312.23(b)"),
        "loa_expiration_or_revocation_terms": ("manufacturer.loa_expiration_terms", "21 CFR 312.23(b)"),
        "loa_signatory": ("manufacturer.loa_signatory", "FDCA 561A; 21 CFR 312.23(b)"),
    }
    return _render("manufacturer-letter-of-authorization", _LOA_TEMPLATE, sources,
                   doc_registry, study, literals=literals)


# ---------------------------------------------------------------------------
# Manufacturer LOA-request (physician -> manufacturer)  —  spec §4.2
# ---------------------------------------------------------------------------

_LOA_REQUEST_TEMPLATE = """\
REQUEST FOR DRUG SUPPLY AND LETTER OF AUTHORIZATION                  [DRAFT]
Authority: FDCA 561A; 21 CFR 312.23(b), 312.305(b)(1)
[Draft for the physician to send to the manufacturer's expanded-access /
 Medical Affairs intake. OSSICRO never auto-sends (Constitution HC1).]

{{request_date}}

URGENCY: {{urgency}}

To: {{manufacturer_name}} — Expanded Access / Medical Affairs

From: {{investigator_name}}{{degrees_suffix}}, {{investigator_address}}
      {{investigator_phone}}   {{investigator_email}}
      Medical license: {{license_number}} ({{license_state}})

Re: Single-patient expanded access request — {{drug_name}}

1. I am treating a patient ({{patient_initials_coded}}, age {{patient_age}},
   sex {{patient_sex}}) with a serious or immediately life-threatening
   condition for which there is no comparable or satisfactory alternative
   therapy. Diagnosis: {{diagnosis}}

2. I request that {{manufacturer_name}} SUPPLY {{drug_name}} for single-patient
   treatment use under its expanded access policy (FDCA 561A).
   Quantity requested: {{quantity_requested}}
   Shipping destination (treatment facility): {{site_name}}

3. I request that {{manufacturer_name}} ISSUE A LETTER OF AUTHORIZATION allowing
   FDA to cross-reference {{ind_dmf_reference}} for CMC and pharmacology/
   toxicology information (21 CFR 312.23(b), 312.305(b)(1)).

4. Treatment plan summary (for supply assessment):
   Dose: {{dose}}   Route: {{route}}   Planned duration: {{duration}}

5. IRB status: {{irb_name}} — {{irb_pathway}}

6. Charging / cost recovery (%(cite_charging)s): {{cost_recovery_statement}}

7. FDA authorization of expanded access does NOT obligate supply. The supply
   decision, the LOA signature, and any fair-market-value / anti-kickback
   judgment (42 U.S.C. 1320a-7b) are the manufacturer's alone (FDCA 561A).

Respectfully,
{{investigator_name}}{{degrees_suffix}}
""" % {
    # M15/P4: first appearance of 21 CFR 312.8 in a rendered document —
    # routed through the single-source citation table (P1 discipline), never
    # string-literal'd here.
    "cite_charging": _C("charging.expanded_access"),
}


def gen_loa_request(study: Study, doc_registry: Dict[str, dict],
                    as_of: Optional[datetime.date] = None) -> Document:
    degrees = study.resolve("investigator.degrees")
    # M15 urgency literal — computed from the SAME emergency parse the cover
    # letter uses (_is_emergency) plus the physician-entered needed-by date.
    # Computed from recorded facts; OSSICRO never invents urgency.
    emergency = _is_emergency(study)
    urgency = "EMERGENCY REQUEST (21 CFR 312.310(d))" if emergency else "Non-emergency request"
    needed_by = study.resolve("submission.needed_by_date")
    if needed_by:
        urgency += " — drug needed by %s (physician-entered)" % needed_by
    # IRB status line: the same pathway facts gen_irb_request renders.
    chair = str(study.resolve("irb.chair_concurrence") or "").strip().lower() in ("true", "1", "yes")
    if emergency:
        irb_pathway = ("emergency-use pathway: IRB notified within 5 working days "
                       "of first treatment (%s)" % _C("clock.irb_emergency_notification"))
    elif chair:
        irb_pathway = ("chair-concurrence pathway requested in lieu of a convened "
                       "board (21 CFR 56.105)")
    else:
        irb_pathway = "standard pathway: IRB approval before treatment (21 CFR Part 56)"
    literals = {
        "request_date": _anchor_literal(as_of, "FDCA 561A"),
        "degrees_suffix": (_degrees_suffix(study.resolve("investigator.name"), degrees),
                           "21 CFR 312.310(a)",
                           "computed from investigator.degrees; omitted if the name already carries the credential"),
        "urgency": (urgency, "21 CFR 312.310(d); FDCA 561A",
                    "computed from submission.emergency + submission.needed_by_date"),
        "irb_pathway": (irb_pathway, "21 CFR 56.104(c)/56.105",
                        "computed from submission.emergency / irb.chair_concurrence"),
    }
    sources = {
        "manufacturer_name": ("manufacturer.name", "FDCA 561A"),
        "investigator_name": ("investigator.name", "21 CFR 312.310(a)"),
        "investigator_address": ("investigator.address", "Form FDA 3926"),
        "investigator_phone": ("investigator.phone", "Form FDA 3926"),
        "investigator_email": ("investigator.email", "Form FDA 3926"),
        "license_number": ("investigator.license_number", "21 CFR 312.310(a)"),
        "license_state": ("investigator.license_state", "21 CFR 312.310(a)"),
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.310"),
        "patient_age": ("patient.age", "21 CFR 312.305(a)"),
        "patient_sex": ("patient.sex", "21 CFR 312.305(a)"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
        "ind_dmf_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "quantity_requested": ("drug.quantity_requested", "FDCA 561A"),
        "site_name": ("site.name", _C("ea.treatment_plan.facility")),
        "irb_name": ("irb.name", "21 CFR 56.104/.105"),
        "cost_recovery_statement": ("submission.cost_recovery_statement",
                                    _C("charging.expanded_access")),
        "dose": ("drug.dose", _C("ea.treatment_plan.dosing")),
        "route": ("drug.route", _C("ea.treatment_plan.dosing")),
        "duration": ("drug.duration", _C("ea.treatment_plan.dosing")),
    }
    return _render("manufacturer-loa-request", _LOA_REQUEST_TEMPLATE, sources,
                   doc_registry, study, literals=literals)


# ---------------------------------------------------------------------------
# IRB concurrence request (§56.105 chair pathway)  —  spec §5
# ---------------------------------------------------------------------------

_IRB_REQUEST_TEMPLATE = """\
IRB CONCURRENCE REQUEST                                              [DRAFT]
Authority: 21 CFR 56.104(c), 56.105, 312.66

{{request_date}}

To: {{irb_name}}
    {{irb_address}}

Re: Single-patient expanded access — {{drug_name}} — patient {{patient_initials_coded}}

I, {{investigator_name}}, request IRB review for expanded-access treatment use of
{{drug_name}} in one patient with {{diagnosis}} (21 CFR 312.310).

{{pathway_statement}}

{{consent_statement}}

   [EXTERNAL-PARTY ACT — gate: irb-approval. The IRB renders the approval or
    chair-concurrence judgment. OSSICRO assembles the request and tracks status;
    it never approves on the IRB's behalf (21 CFR 56.108-56.111).]

{{investigator_name}}
"""


def _consent_statement(study: Study, emergency: bool) -> Optional[str]:
    """M14 (Overhaul P5): the pathway-TRUE consent sentence for the IRB
    request, computed from the route's emergency flag and the physician's
    ``consent.timing_attestation`` — never a fixed assertion that is false
    on the emergency route (where treatment may lawfully precede consent
    under the 21 CFR 50.23 exception).

    Returns None when the sentence cannot be computed honestly (emergency
    route with no recorded attestation) — the caller renders the explicit
    MISSING marker naming the intake field (HC2: never assert what was not
    entered).
    """
    if not emergency:
        # Standard pathway: consent precedes treatment by construction.
        return ("Informed consent per 21 CFR Part 50 will be obtained "
                "before treatment begins.")
    attestation = str(study.resolve("consent.timing_attestation") or "").strip()
    if attestation == "obtained-before-treatment":
        return ("Informed consent per 21 CFR Part 50 was obtained before "
                "the emergency treatment began (physician attestation: "
                "obtained-before-treatment).")
    if attestation == "exception-50.23-documented":
        return ("Informed consent was not obtained before this emergency "
                "use; the physician has documented the exception from the "
                "informed-consent requirements under %s."
                % _C("consent.emergency_exception"))
    if attestation == "not-yet-obtained":
        return ("Informed consent per 21 CFR Part 50 has NOT yet been "
                "obtained (physician attestation: not-yet-obtained); it "
                "must be obtained before treatment unless the %s exception "
                "is documented." % _C("consent.emergency_exception"))
    return None   # absent (or unrecognized) attestation -> honest MISSING


def gen_irb_request(study: Study, doc_registry: Dict[str, dict],
                    as_of: Optional[datetime.date] = None) -> Document:
    emergency = _is_emergency(study)
    chair = str(study.resolve("irb.chair_concurrence") or "").strip().lower() in ("true", "1", "yes")
    if emergency:
        ftd = study.resolve("submission.first_treatment_date")
        deadline = compute_deadline(ftd, 5, "working",
                                    field_id="submission.first_treatment_date")
        if deadline:
            pathway = ("EMERGENCY USE (%s): treatment may proceed before IRB "
                       "review provided the IRB is notified within 5 WORKING DAYS of the "
                       "first treatment (%s); that deadline is %s."
                       % (_C("clock.irb_emergency_notification"), ftd, deadline))
        else:
            pathway = ("EMERGENCY USE (%s): enter the first-treatment date so "
                       "OSSICRO can compute the 5-working-day IRB-notification deadline."
                       % _C("clock.irb_emergency_notification"))
    elif chair:
        pathway = ("The physician requests IRB CHAIRPERSON (or designated member) "
                   "CONCURRENCE in lieu of a convened full board, per 21 CFR 56.105 "
                   "(Form 3926 Field 10.b), before treatment begins.")
    else:
        pathway = ("Standard pathway: IRB APPROVAL is requested before treatment begins "
                   "(21 CFR Part 56).")
    literals = {
        "request_date": _anchor_literal(as_of, "21 CFR 56.109"),
        "pathway_statement": (pathway, "21 CFR 56.104(c)/56.105", "computed from submission.emergency / irb.chair_concurrence"),
    }
    # M14: the consent sentence is COMPUTED from route + attestation
    # (pathway-true), provenance-stamped like pathway_statement. When it
    # cannot be computed honestly (emergency, no attestation) the span
    # renders the explicit MISSING marker naming the intake field to fill —
    # never a fixed sentence that may be false on this route (HC2).
    template = _IRB_REQUEST_TEMPLATE
    consent_stmt = _consent_statement(study, emergency)
    if consent_stmt is None:
        template = template.replace(
            "{{consent_statement}}",
            MISSING_MARKER % "consent.timing_attestation")
    else:
        literals["consent_statement"] = (
            consent_stmt,
            "%s; %s" % (_C("consent.general_requirements"),
                        _C("consent.emergency_exception")),
            "computed from submission.emergency + consent.timing_attestation")
    sources = {
        "irb_name": ("irb.name", "21 CFR 56.104/.105"),
        "irb_address": ("irb.address", "21 CFR 56.104/.105"),
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.310"),
        "investigator_name": ("investigator.name", "21 CFR 312.66"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
    }
    return _render("irb-concurrence-request", template, sources,
                   doc_registry, study, literals=literals)


# ---------------------------------------------------------------------------
# Drug-accountability shell  —  spec generator list; filled at dispensing
# ---------------------------------------------------------------------------

_DRUG_ACCT_TEMPLATE = """\
INVESTIGATIONAL PRODUCT ACCOUNTABILITY LOG (SHELL)                   [DRAFT]
Authority: 21 CFR 312.62(a), 312.61

Drug: {{drug_name}}

+------------+------------+----------+-----------+-----------+------------------+
| Date       | Lot number | Received | Dispensed | Returned  | Balance / initial|
+------------+------------+----------+-----------+-----------+------------------+
|            | {{lot_numbers}}         |           |           |                  |
+------------+------------+----------+-----------+-----------+------------------+
Dispensing entries: {{dispensing_entries}}

[SHELL — deliberately a shell to be filled at dispensing (M7): lot numbers and
 dispensing entries are recorded at the bedside once the manufacturer ships the
 drug; they are honestly absent at submission time and are not intake fields —
 post-supply record-keeping sits outside this drafting product's scope (see the
 document registry entry).]
"""


def gen_drug_accountability(study: Study, doc_registry: Dict[str, dict],
                            as_of: Optional[datetime.date] = None) -> Document:
    sources = {
        "drug_name": ("drug.name", "21 CFR 312.62(a)"),
        "lot_numbers": ("drug.lot_numbers", "21 CFR 312.62(a)"),
        "dispensing_entries": ("drug.dispensing_entries", "21 CFR 312.62(a)"),
    }
    return _render("drug-accountability-log", _DRUG_ACCT_TEMPLATE, sources, doc_registry, study)


# ---------------------------------------------------------------------------
# ICF — delegate to the built-in generator (keeps the 8 verbatim 50.25 spans
# and their SHA-256-verified provenance intact for rule R-ICF-50.25).
# ---------------------------------------------------------------------------

def gen_icf(study: Study, doc_registry: Dict[str, dict],
            as_of: Optional[datetime.date] = None) -> Document:
    # The built-in ICF template carries no engine-stamped date span; as_of is
    # accepted for dispatch uniformity and unused.
    return builtin_generate.generate_document(study, "informed-consent-form-part50", doc_registry)


# ---------------------------------------------------------------------------
# EA-profiled informed-consent form (Overhaul P6; closes M3/m10/m9/m12's
# document half). Both 3926 routes render THIS form; the generic
# informed-consent-form-part50 stays registered for non-EA routes.
#
# HITL — the package-level hard requirement: consent language a real patient
# would sign requires review by a qualified, IRB-experienced human. The
# template ships to the best-known target (FDA's individual-patient expanded-
# access guidance) and the draft banner below stays on the artifact until
# that human review removes it. Heading-completeness (R-ICF-50.25-EA) is NOT
# adequacy — adequacy is the deferred concept rule R-ICF-50.25-ADEQ-EA plus
# the human pass.
# ---------------------------------------------------------------------------

# The one banner line (spec wording). Removed ONLY by the qualified human
# review — never by code.
ICF_EA_PENDING_BANNER = (
    "PENDING-HUMAN-VERIFICATION — consent language not yet reviewed by a "
    "qualified human")

# The treatment-use framing per FDA's individual-patient EA guidance: it
# resolves the therapeutic misconception in BOTH directions (this is
# treatment, not research — and the research-protection laws still apply).
# Rendered as a computed literal so its guidance citation rides in the
# provenance record, not in the patient-facing prose.
_ICF_EA_FRAMING = (
    "You are being asked to receive treatment with an investigational drug "
    "under the FDA's expanded access (\"compassionate use\") program. This "
    "is treatment, not a research study, but laws that protect research "
    "participants also protect you.")

# 50.25(b)(4): consequences of a decision to stop, and orderly termination.
_ICF_EA_STOPPING = (
    "Stopping is your choice at any time. If you decide to stop, tell your "
    "doctor first so that stopping can be planned safely: with some drugs, "
    "stopping suddenly can be harmful, and your doctor may recommend "
    "follow-up visits or tests after the last dose.")

# 50.25(b)(5): significant new findings.
_ICF_EA_NEW_FINDINGS = (
    "You will be told about any significant new findings learned during "
    "your treatment that may affect your willingness to continue.")

_ICF_EA_TEMPLATE = """\
INFORMED CONSENT FORM — INDIVIDUAL-PATIENT EXPANDED ACCESS            [DRAFT]
Authority: 21 CFR 50.25 (elements), 21 CFR 50.27 (documentation); 21 CFR 312.305(c)
STATUS: draft for IRB review. The consent EVENT is a non-delegable human
act between the physician and the patient (gate: informed-consent).
[%(pending_banner)s (IRB-experienced).
 This line is removed only by that human review; heading-completeness is
 NOT adequacy (deferred rule R-ICF-50.25-ADEQ-EA).]

Treatment plan: {{plan_title}}
Plan identifier: {{protocol_number}} v{{protocol_version}}
Treating physician: {{investigator_name}}, {{site_name}}

WHAT THIS IS. {{treatment_framing}}

1. RESEARCH STATEMENT, PURPOSE, DURATION, PROCEDURES - 50.25(a)(1)
   This expanded access use is treatment with {{drug_name}}, an
   investigational drug. Purpose: {{purpose}}
   Expected duration of treatment: {{consent_duration}}
   Procedures (experimental procedures identified): {{procedures}}

2. REASONABLY FORESEEABLE RISKS OR DISCOMFORTS - 50.25(a)(2)
   {{risks}}

3. BENEFITS THAT MAY REASONABLY BE EXPECTED - 50.25(a)(3)
   {{benefits}}

4. APPROPRIATE ALTERNATIVE PROCEDURES OR TREATMENTS - 50.25(a)(4)
   {{alternatives}}

5. CONFIDENTIALITY OF RECORDS - 50.25(a)(5)
   {{confidentiality_statement}} Records may be inspected by the FDA.

6. COMPENSATION AND MEDICAL TREATMENT FOR INJURY - 50.25(a)(6)
   {{injury_compensation_statement}}
   If you believe you have been injured as a result of this treatment,
   contact {{injury_contact_name}} at {{injury_contact_phone}}.

7. WHOM TO CONTACT - 50.25(a)(7)
   Questions about the treatment: {{research_contact}}.
   Questions about your rights: {{irb_name}}, {{irb_phone}}.

8. VOLUNTARY PARTICIPATION - 50.25(a)(8)
   Receiving this treatment is voluntary. You may refuse it, and you may
   stop it at any time, without penalty or loss of benefits to which you
   are otherwise entitled.

EXPANDED-ACCESS DISCLOSURES

A. INVESTIGATIONAL STATUS — NOT FDA-APPROVED. {{drug_name}} is not approved
   by the FDA for your condition. The FDA's permission for this expanded
   access use is NOT evidence that the drug works or that it is safe for
   your condition.

B. DRUG SUPPLY. The manufacturer, {{manufacturer_name}}, decides whether to
   provide the drug. It may decline to supply it, or stop supplying it, at
   any time.

C. COSTS TO YOU — %(cite_costs)s
   {{cost_statement}}

D. STOPPING TREATMENT — %(cite_stopping)s
   {{stopping_treatment}}

E. NEW INFORMATION — %(cite_new_findings)s
   {{significant_new_findings}}

F. YOUR CHOICE, RESTATED — 21 CFR 50.25(a)(8)
   Whether to start this treatment, and whether to continue it, is your
   decision. Refusing or stopping will not affect the regular medical care
   you are otherwise entitled to receive.

SIGNATURE OF PATIENT: ______________________  DATE: ____________
PERSON OBTAINING CONSENT: __________________  DATE: ____________
   [NON-DELEGABLE HUMAN ACT - gate: informed-consent. This engine
    drafts the form; consent itself is obtained by a qualified human.]
""" % {
    "pending_banner": ICF_EA_PENDING_BANNER,
    # P1 discipline: the additional-element pinpoints come from the single-
    # source table, never string-literal'd here.
    "cite_costs": "%s; %s" % (_C("consent.element_costs"),
                              _C("charging.consent_disclosure")),
    "cite_stopping": _C("consent.element_stopping"),
    "cite_new_findings": _C("consent.element_new_findings"),
}

# span -> (dotted study path, citation). Exported so the app's fix-loop
# span->field map can consume it directly (one authored copy); the same dict
# is the generator's sources table below.
ICF_EA_FIELD_SOURCES: Dict[str, Tuple[str, str]] = {
    "plan_title": ("title", "21 CFR 50.20"),
    "protocol_number": ("protocol_number", "21 CFR 50.20"),
    "protocol_version": ("protocol_version", "21 CFR 50.20"),
    "investigator_name": ("investigator.name", "21 CFR 50.25(a)(7)"),
    "site_name": ("site.name", "21 CFR 50.20"),
    "drug_name": ("drug.name", "21 CFR 312.305(b)"),
    "manufacturer_name": ("manufacturer.name", "FDCA 561A"),
    "purpose": ("consent.purpose", "21 CFR 50.25(a)(1)"),
    "consent_duration": ("consent.duration", "21 CFR 50.25(a)(1)"),
    "procedures": ("consent.procedures", "21 CFR 50.25(a)(1)"),
    "risks": ("consent.risks", "21 CFR 50.25(a)(2)"),
    "benefits": ("consent.benefits", "21 CFR 50.25(a)(3)"),
    "alternatives": ("consent.alternatives", "21 CFR 50.25(a)(4)"),
    "confidentiality_statement": ("consent.confidentiality_statement",
                                  "21 CFR 50.25(a)(5)"),
    # M3: element 6 becomes SATISFIABLE — it renders the P2 intake field
    # consent.injury_compensation_statement; absent -> [[MISSING: ...]] and
    # the ledger question routes to that intake field.
    "injury_compensation_statement": ("consent.injury_compensation_statement",
                                      _C("consent.element_injury_compensation")),
    "injury_contact_name": ("contacts.injury_contact_name",
                            _C("consent.element_injury_compensation")),
    "injury_contact_phone": ("contacts.injury_contact_phone",
                             _C("consent.element_injury_compensation")),
    "research_contact": ("contacts.research_contact", "21 CFR 50.25(a)(7)"),
    "irb_name": ("irb.name", "21 CFR 50.25(a)(7)"),
    "irb_phone": ("irb.phone", "21 CFR 50.25(a)(7)"),
    # 50.25(b)(3) + 312.8(d): whether the patient may be charged.
    "cost_statement": ("consent.cost_statement",
                       "%s; %s" % (_C("consent.element_costs"),
                                   _C("charging.consent_disclosure"))),
}


def gen_icf_ea(study: Study, doc_registry: Dict[str, dict],
               as_of: Optional[datetime.date] = None) -> Document:
    """The EA-profiled informed-consent draft (P6).

    ``as_of`` is accepted for dispatch uniformity and unused (the consent
    form carries no engine-stamped date span — the consent date is written
    by the humans at the consent event).
    """
    literals = {
        "treatment_framing": (_ICF_EA_FRAMING,
                              _C("ea.consent.treatment_framing"),
                              "fixed treatment-use framing (FDA individual-"
                              "patient EA guidance); pending human review "
                              "per the document banner"),
        "stopping_treatment": (_ICF_EA_STOPPING,
                               _C("consent.element_stopping"),
                               "fixed 50.25(b)(4) stopping-treatment "
                               "disclosure; pending human review per the "
                               "document banner"),
        "significant_new_findings": (_ICF_EA_NEW_FINDINGS,
                                     _C("consent.element_new_findings"),
                                     "fixed 50.25(b)(5) new-findings "
                                     "disclosure; pending human review per "
                                     "the document banner"),
    }
    doc = _render("informed-consent-form-part50-ea", _ICF_EA_TEMPLATE,
                  ICF_EA_FIELD_SOURCES, doc_registry, study, literals=literals)
    # Stamp provenance for the eight verbatim-locked 50.25(a) element
    # headings (BYTE-IDENTICAL to the generic form — same tuples, aliased in
    # generate.VERBATIM_SPANS) so rule R-ICF-50.25-EA verifies presence and
    # SHA-256 identity exactly as R-ICF-50.25 does for the generic form.
    for span_id, (span_text, span_citation) in builtin_generate.VERBATIM_SPANS[
            "informed-consent-form-part50-ea"].items():
        if span_text in doc.rendered:
            doc.provenance.append(ProvenanceRecord(
                span=span_id,
                source="template:informed-consent-form-part50-ea#%s" % span_id,
                citation=span_citation))
    return doc


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_GENERATORS: Dict[str, Callable[..., Document]] = {
    "expanded-access-cover-letter": gen_cover_letter,
    "form-fda-3926-individual-patient-expanded-access": gen_form_3926,
    "expanded-access-treatment-plan": gen_treatment_plan,
    "manufacturer-letter-of-authorization": gen_loa,
    "manufacturer-loa-request": gen_loa_request,
    "irb-concurrence-request": gen_irb_request,
    "drug-accountability-log": gen_drug_accountability,
    "informed-consent-form-part50": gen_icf,
    "informed-consent-form-part50-ea": gen_icf_ea,
}


def generate_route_documents(study: Study, route: Dict[str, object],
                             doc_registry: Dict[str, dict],
                             as_of: Optional[datetime.date] = None) -> Dict[str, Document]:
    """Generate every document the route declares, in the route's order.

    A doc id with no registered EA generator is skipped (its absence surfaces as
    a red 'missing document' ledger item, not a crash). ``as_of`` anchors the
    documents' dated spans; when omitted it is derived from the physician-
    entered trigger dates (never the wall clock), and when no anchor exists the
    dated spans render as MISSING markers.
    """
    if as_of is None:
        as_of = derive_as_of(study)
    docs: Dict[str, Document] = {}
    for doc_id in route.get("documents", []):
        gen = _GENERATORS.get(doc_id)
        if gen is None:
            continue
        docs[doc_id] = gen(study, doc_registry, as_of=as_of)
    return docs
