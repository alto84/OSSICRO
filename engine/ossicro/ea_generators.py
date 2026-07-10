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

from . import generate as builtin_generate
from .clocks import (
    add_working_days,
    expanded_access_emergency_deadlines,
    federal_holidays,
    ind_30_day_deadline,
)
from .models import Document, ProvenanceRecord, Study

_PLACEHOLDER = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
MISSING_MARKER = "[[MISSING: %s]]"


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
# ``expanded_access_emergency_deadlines`` and ``ind_30_day_deadline`` are
# re-exported from clocks so callers (and tests) reach one source of truth.
# ---------------------------------------------------------------------------

__all__ = [
    "add_working_days",
    "federal_holidays",
    "expanded_access_emergency_deadlines",
    "ind_30_day_deadline",
    "compute_deadline",
    "compute_clocks",
    "build_study",
    "unflatten",
    "generate_route_documents",
]


def _parse_date(text: Optional[str]) -> Optional[datetime.date]:
    if not text:
        return None
    text = str(text).strip()[:10]
    try:
        return datetime.datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def compute_deadline(trigger: Optional[str], days: int, calendar: str) -> Optional[str]:
    """Return the ISO deadline for a trigger date, or None if no trigger given.

    ``working`` days route through the canonical ossicro.clocks engine (weekends
    + observed federal holidays); ``calendar`` days are a plain span.
    """
    start = _parse_date(trigger)
    if start is None:
        return None
    if calendar == "working":
        return add_working_days(start, days).isoformat()
    return (start + datetime.timedelta(days=days)).isoformat()


def compute_clocks(study: Study, route: Dict[str, object]) -> List[Dict[str, object]]:
    """Compute every clock the route arms. Trigger dates are human-entered.

    A clock with no trigger date entered is returned ``armed=False`` with a null
    deadline and the resolving question naming the trigger — honestly pending,
    never guessed.
    """
    out: List[Dict[str, object]] = []
    for clock in route.get("clocks", []):
        trigger_field = clock["trigger_field"]
        trigger_value = study.resolve(trigger_field)
        # The 30-day IND clock defaults its trigger to the submission date.
        if trigger_value is None and clock["id"] == "ind-effective-30-day":
            trigger_value = study.resolve("submission.date") or datetime.date.today().isoformat()
        deadline = compute_deadline(trigger_value, clock["days"], clock["calendar"])
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
            "armed": deadline is not None,
            "note": clock.get("note", ""),
        })
    return out


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
            if value is None or str(value).strip() == "":
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
   condition — {{diagnosis}} — for which there is no comparable or satisfactory
   alternative therapy.

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
   Letter of Authorization; IRB concurrence evidence; informed consent form.

7. CONTACT. {{investigator_name}}, {{investigator_phone}}, {{investigator_email}}.
   IRB of record: {{irb_name}}.

Respectfully submitted,

______________________________________________  Date: __________
{{investigator_name}}{{degrees_suffix}}
   [NON-DELEGABLE HUMAN ACT — gate: submission-to-fda. OSSICRO drafts this
    letter; only the sponsor-investigator signs and files it. 21 CFR 312.20,
    312.23, 312.40.]
"""


def gen_cover_letter(study: Study, doc_registry: Dict[str, dict]) -> Document:
    degrees = study.resolve("investigator.degrees")
    emergency = str(study.resolve("submission.emergency") or "").strip().lower() in ("true", "1", "yes")
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
        auth_date = _parse_date(auth)
        if auth_date is not None:
            # The 15-working-day written-3926 clock is the canonical emergency
            # deadline pair's first entry (21 CFR 312.310(d)(2)).
            written = expanded_access_emergency_deadlines(auth_date)[0]
            clock_statement = (
                "This written submission is filed within 15 WORKING DAYS of the FDA "
                "telephone authorization dated %s; that deadline is %s (21 CFR "
                "312.310(d))." % (auth, written.due.isoformat())
            )
        else:
            clock_statement = (
                "EMERGENCY: enter the FDA telephone-authorization date so OSSICRO can "
                "compute the 15-working-day written-3926 deadline (21 CFR 312.310(d))."
            )
        clock_cite = "21 CFR 312.310(d)"
    else:
        receipt = study.resolve("submission.fda_receipt_date")
        receipt_date = _parse_date(receipt) or datetime.date.today()
        deadline = ind_30_day_deadline(receipt_date).due.isoformat()
        clock_statement = (
            "For a non-emergency request, treatment may not begin until FDA notifies "
            "the physician it may proceed, or — absent notification — 30 CALENDAR DAYS "
            "after FDA receipt (%s), i.e. %s (21 CFR 312.40(b)(1))."
            % (receipt or "FDA receipt", deadline)
        )
        clock_cite = "21 CFR 312.40(b)(1)"

    literals = {
        "cover_date": (datetime.date.today().isoformat(), "21 CFR 312.23(a)(1)", "computed: today"),
        "submission_kind": (submission_kind, "Form FDA 3926", "computed from submission.* intake"),
        "degrees_suffix": ((", " + degrees) if degrees else "", "21 CFR 312.310(a)", "computed from investigator.degrees"),
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
# ---------------------------------------------------------------------------

_FORM_3926_TEMPLATE = """\
FORM FDA 3926 — INDIVIDUAL PATIENT EXPANDED ACCESS IND               [DRAFT]
Authority: 21 CFR 312.310; Form FDA 3926 (OMB 0910-0814)

 1. DATE OF SUBMISSION: {{submission_date}}
 2. TYPE OF SUBMISSION: {{submission_kind}}   (IND #: {{ind_number}})
 3. PATIENT INFORMATION AND CLINICAL PRESENTATION
    Patient identifier (coded — no direct identifiers): {{patient_initials_coded}}
    Age: {{patient_age}}   Sex: {{patient_sex}}
    Diagnosis / condition: {{diagnosis}}
    Prior therapies and outcomes: {{prior_therapies}}
    Clinical rationale (seriousness; no satisfactory alternative; benefit
    justifies risk — 21 CFR 312.305(a)): {{clinical_rationale}}
 4. INVESTIGATIONAL DRUG
    Name: {{drug_name}}     Manufacturer / source: {{manufacturer_name}}
 5. TREATMENT PLAN (summary; full plan attached)
    {{treatment_plan_summary}}
    Dose: {{dose}}   Route: {{route}}   Planned duration: {{duration}}
    Monitoring: {{monitoring_plan}}
 6. LETTER OF AUTHORIZATION
    LOA cross-references application: {{loa_reference}}
 7. PHYSICIAN QUALIFICATION STATEMENT
    {{physician_name}}{{degrees_suffix}}; license {{license_number}} ({{license_state}}).
    §312.310(a) determination (risk drug <= risk disease): {{risk_determination}}
 8. INSTITUTIONAL REVIEW BOARD
    IRB of record: {{irb_name}}
10.a WAIVER (§312.10 — waive additional Part 312 / Forms 1571 & 1572
    requirements): {{waiver_10a}}
10.b WAIVER (§56.105 — IRB chairperson concurrence in lieu of convened board):
    {{waiver_10b}}
    [Fields 10.a / 10.b are physician attestations; OSSICRO never defaults or
     auto-checks them.]

11. PHYSICIAN (REQUESTOR / SPONSOR-INVESTIGATOR)
    {{physician_name}}{{degrees_suffix}}
    {{physician_address}}
    {{physician_phone}}   {{physician_email}}
    SIGNATURE: ____________________________________  DATE: __________
   [NON-DELEGABLE HUMAN ACT — gate: submission-to-fda. Software cannot be a
    sponsor (21 CFR 312.52) and cannot execute this signature or file the form.]
"""


def _bool_label(study: Study, path: str) -> str:
    raw = study.resolve(path)
    if raw is None:
        return ""  # unanswered -> renders MISSING, honestly
    return "CHECKED (physician-attested)" if str(raw).strip().lower() in ("true", "1", "yes") else "not checked"


def gen_form_3926(study: Study, doc_registry: Dict[str, dict]) -> Document:
    degrees = study.resolve("investigator.degrees")
    initial = (study.resolve("submission.initial_or_followup") or "initial").strip().lower()
    emergency = str(study.resolve("submission.emergency") or "").strip().lower() in ("true", "1", "yes")
    kind = ("(b) Initial — EMERGENCY use (21 CFR 312.310(d))" if emergency
            else "(a) Initial application") if initial != "followup" else "(c) Follow-up submission"
    # Compose the treatment-plan summary and clinical rationale required fields.
    literals = {
        "submission_date": (datetime.date.today().isoformat(), "Form FDA 3926 field 1", "computed: today"),
        "submission_kind": (kind, "Form FDA 3926 field 2; 21 CFR 312.310(d)", "computed from submission.* intake"),
        "degrees_suffix": ((", " + degrees) if degrees else "", "21 CFR 312.310(a)", "computed from investigator.degrees"),
        "waiver_10a": (_bool_label(study, "waiver_10a"), "21 CFR 312.10", "physician attestation: waiver_10a"),
        "waiver_10b": (_bool_label(study, "waiver_10b"), "21 CFR 56.105", "physician attestation: waiver_10b"),
    }
    sources = {
        "ind_number": ("submission.ind_number", "Form FDA 3926 field 2"),
        "patient_initials_coded": ("patient.coded_id", "Form FDA 3926 field 3; 21 CFR 312.310"),
        "patient_age": ("patient.age", "Form FDA 3926 field 3"),
        "patient_sex": ("patient.sex", "Form FDA 3926 field 3"),
        "diagnosis": ("patient.diagnosis", "Form FDA 3926 field 3; 21 CFR 312.305(a)(1)"),
        "prior_therapies": ("patient.prior_therapies", "21 CFR 312.310(a)"),
        "clinical_rationale": ("request.clinical_rationale", "21 CFR 312.305(a); 312.310(a)"),
        "drug_name": ("drug.name", "Form FDA 3926 field 4"),
        "manufacturer_name": ("manufacturer.name", "Form FDA 3926 field 4"),
        "treatment_plan_summary": ("treatment.benefit_risk", "21 CFR 312.305(b)(2)(iii)"),
        "dose": ("drug.dose", "21 CFR 312.305(b)(2)(iii)"),
        "route": ("drug.route", "21 CFR 312.305(b)(2)(iii)"),
        "duration": ("drug.duration", "21 CFR 312.305(b)(2)(iii)"),
        "monitoring_plan": ("treatment.monitoring_plan", "21 CFR 312.305(b)(2)(vii)"),
        "loa_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "physician_name": ("investigator.name", "Form FDA 3926 field 10; 21 CFR 312.310(a)"),
        "license_number": ("investigator.license_number", "21 CFR 312.310(a)"),
        "license_state": ("investigator.license_state", "21 CFR 312.310(a)"),
        "risk_determination": ("investigator.risk_determination", "21 CFR 312.310(a)"),
        "irb_name": ("irb.name", "21 CFR Part 56"),
        "physician_address": ("investigator.address", "Form FDA 3926 field 10"),
        "physician_phone": ("investigator.phone", "Form FDA 3926 field 10"),
        "physician_email": ("investigator.email", "Form FDA 3926 field 10"),
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

1. RATIONALE FOR TREATMENT USE — 21 CFR 312.305(b)(2)(i)
   {{treatment_rationale}}

2. PATIENT DESCRIPTION AND SELECTION — 21 CFR 312.305(b)(2)(ii)
   Coded patient: {{patient_initials_coded}}   Diagnosis: {{diagnosis}}
   Prior therapies and responses: {{prior_therapies}}
   No comparable/satisfactory alternative — basis: {{no_alternative_basis}}

3. METHOD OF ADMINISTRATION, DOSE, AND DURATION — 21 CFR 312.305(b)(2)(iii)
   {{dosing_plan}}
   Route/method: {{route}}   Planned duration: {{duration}}

4. FACILITY AND PERSONNEL — 21 CFR 312.305(b)(2)(iv)
   Treatment facility: {{facility}}

5. CMC; PHARMACOLOGY/TOXICOLOGY — 21 CFR 312.305(b)(2)(v)-(vi)
   Incorporated by reference to {{loa_reference}} per the attached LOA
   (21 CFR 312.23(b)); the physician does not author CMC/nonclinical content.

6. MONITORING PLAN — 21 CFR 312.305(b)(2)(vii)
   {{monitoring_plan}}

7. SAFETY REPORTING — 21 CFR 312.305(c), 312.310(c), 312.32
   The sponsor-investigator will report serious, unexpected, suspected adverse
   reactions to FDA per 21 CFR 312.32 and provide the summary/annual report per
   21 CFR 312.310(c)(2). Causality/expectedness is the medical monitor's
   non-delegable judgment (gate: sae-causality).

Treating physician (sponsor-investigator): {{physician_name}}
Signature: ______________________________  Date: __________
"""


def gen_treatment_plan(study: Study, doc_registry: Dict[str, dict]) -> Document:
    dose = study.resolve("drug.dose")
    route = study.resolve("drug.route")
    duration = study.resolve("drug.duration")
    dosing_bits = [b for b in [dose and ("Dose: " + dose), route and ("Route: " + route),
                               duration and ("Duration: " + duration)] if b]
    literals = {}
    if dosing_bits:
        literals["dosing_plan"] = ("; ".join(dosing_bits), "21 CFR 312.305(b)(2)(iii)",
                                   "composed from drug.dose/route/duration")
    sources = {
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "physician_name": ("investigator.name", "21 CFR 312.305(c)"),
        "loa_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "treatment_rationale": ("request.clinical_rationale", "21 CFR 312.305(b)(2)(i); 312.305(a)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.305(b)(2)(ii)"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(b)(2)(ii)"),
        "prior_therapies": ("patient.prior_therapies", "21 CFR 312.305(b)(2)(ii)"),
        "no_alternative_basis": ("patient.no_alternative_basis", "21 CFR 312.305(a)(1); 312.310(a)(2)"),
        "route": ("drug.route", "21 CFR 312.305(b)(2)(iii)"),
        "duration": ("drug.duration", "21 CFR 312.305(b)(2)(iii)"),
        "facility": ("site.name", "21 CFR 312.305(b)(2)(iv)"),
        "monitoring_plan": ("treatment.monitoring_plan", "21 CFR 312.305(b)(2)(vii)"),
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
 drafts; the physician cannot sign on the manufacturer's behalf.]

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

Authorized party (holder of the right of reference):
  {{authorized_party}}
  {{authorized_party_address}}

Sincerely,

______________________________________________
Authorized official, {{manufacturer_name}}
   [EXTERNAL-PARTY ACT — the manufacturer signs this LOA. OSSICRO records the
    returned LOA as a fact; it never signs or supplies (FDCA 561A).]
"""


def gen_loa(study: Study, doc_registry: Dict[str, dict]) -> Document:
    literals = {
        "loa_date": (datetime.date.today().isoformat(), "21 CFR 312.23(b)", "computed: today"),
    }
    sources = {
        "manufacturer_name": ("manufacturer.name", "21 CFR 312.23(b)"),
        "fda_division": ("submission.fda_division", "21 CFR 312.23(b)"),
        "drug_master_file_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "drug_name": ("drug.name", "21 CFR 312.23(b)"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
        "authorized_party": ("investigator.name", "21 CFR 312.23(b)"),
        "authorized_party_address": ("investigator.address", "21 CFR 312.23(b)"),
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

To: {{manufacturer_name}} — Expanded Access / Medical Affairs

From: {{investigator_name}}{{degrees_suffix}}, {{investigator_address}}
      {{investigator_phone}}   {{investigator_email}}

Re: Single-patient expanded access request — {{drug_name}}

1. I am treating a patient ({{patient_initials_coded}}) with {{diagnosis}}, a
   serious or immediately life-threatening condition with no comparable or
   satisfactory alternative therapy.

2. I request that {{manufacturer_name}} SUPPLY {{drug_name}} for single-patient
   treatment use under its expanded access policy (FDCA 561A).

3. I request that {{manufacturer_name}} ISSUE A LETTER OF AUTHORIZATION allowing
   FDA to cross-reference {{ind_dmf_reference}} for CMC and pharmacology/
   toxicology information (21 CFR 312.23(b), 312.305(b)(1)).

4. Treatment plan summary (for supply assessment):
   Dose: {{dose}}   Route: {{route}}   Planned duration: {{duration}}

5. FDA authorization of expanded access does NOT obligate supply. The supply
   decision, the LOA signature, and any fair-market-value / anti-kickback
   judgment are the manufacturer's alone (FDCA 561A).

Respectfully,
{{investigator_name}}{{degrees_suffix}}
"""


def gen_loa_request(study: Study, doc_registry: Dict[str, dict]) -> Document:
    degrees = study.resolve("investigator.degrees")
    literals = {
        "request_date": (datetime.date.today().isoformat(), "FDCA 561A", "computed: today"),
        "degrees_suffix": ((", " + degrees) if degrees else "", "21 CFR 312.310(a)", "computed from investigator.degrees"),
    }
    sources = {
        "manufacturer_name": ("manufacturer.name", "FDCA 561A"),
        "investigator_name": ("investigator.name", "21 CFR 312.310(a)"),
        "investigator_address": ("investigator.address", "Form FDA 3926"),
        "investigator_phone": ("investigator.phone", "Form FDA 3926"),
        "investigator_email": ("investigator.email", "Form FDA 3926"),
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.310"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
        "ind_dmf_reference": ("manufacturer.ind_dmf_reference", "21 CFR 312.23(b)"),
        "dose": ("drug.dose", "21 CFR 312.305(b)(2)(iii)"),
        "route": ("drug.route", "21 CFR 312.305(b)(2)(iii)"),
        "duration": ("drug.duration", "21 CFR 312.305(b)(2)(iii)"),
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

Informed consent per 21 CFR Part 50 will be obtained before treatment begins.

   [EXTERNAL-PARTY ACT — gate: irb-approval. The IRB renders the approval or
    chair-concurrence judgment. OSSICRO assembles the request and tracks status;
    it never approves on the IRB's behalf (21 CFR 56.108-56.111).]

{{investigator_name}}
"""


def gen_irb_request(study: Study, doc_registry: Dict[str, dict]) -> Document:
    emergency = str(study.resolve("submission.emergency") or "").strip().lower() in ("true", "1", "yes")
    chair = str(study.resolve("irb.chair_concurrence") or "").strip().lower() in ("true", "1", "yes")
    if emergency:
        ftd = study.resolve("submission.first_treatment_date")
        deadline = compute_deadline(ftd, 5, "working")
        if deadline:
            pathway = ("EMERGENCY USE (21 CFR 56.104(c)): treatment may proceed before IRB "
                       "review provided the IRB is notified within 5 WORKING DAYS of the "
                       "first treatment (%s); that deadline is %s." % (ftd, deadline))
        else:
            pathway = ("EMERGENCY USE (21 CFR 56.104(c)): enter the first-treatment date so "
                       "OSSICRO can compute the 5-working-day IRB-notification deadline.")
    elif chair:
        pathway = ("The physician requests IRB CHAIRPERSON (or designated member) "
                   "CONCURRENCE in lieu of a convened full board, per 21 CFR 56.105 "
                   "(Form 3926 Field 10.b), before treatment begins.")
    else:
        pathway = ("Standard pathway: IRB APPROVAL is requested before treatment begins "
                   "(21 CFR Part 56).")
    literals = {
        "request_date": (datetime.date.today().isoformat(), "21 CFR 56.109", "computed: today"),
        "pathway_statement": (pathway, "21 CFR 56.104(c)/56.105", "computed from submission.emergency / irb.chair_concurrence"),
    }
    sources = {
        "irb_name": ("irb.name", "21 CFR 56.104/.105"),
        "irb_address": ("irb.address", "21 CFR 56.104/.105"),
        "drug_name": ("drug.name", "21 CFR 312.305(b)"),
        "patient_initials_coded": ("patient.coded_id", "21 CFR 312.310"),
        "investigator_name": ("investigator.name", "21 CFR 312.66"),
        "diagnosis": ("patient.diagnosis", "21 CFR 312.305(a)(1)"),
    }
    return _render("irb-concurrence-request", _IRB_REQUEST_TEMPLATE, sources,
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

[SHELL — lot numbers and dispensing entries are recorded at the bedside once the
 manufacturer ships the drug; they are honestly absent at submission time.]
"""


def gen_drug_accountability(study: Study, doc_registry: Dict[str, dict]) -> Document:
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

def gen_icf(study: Study, doc_registry: Dict[str, dict]) -> Document:
    return builtin_generate.generate_document(study, "informed-consent-form-part50", doc_registry)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_GENERATORS: Dict[str, Callable[[Study, Dict[str, dict]], Document]] = {
    "expanded-access-cover-letter": gen_cover_letter,
    "form-fda-3926-individual-patient-expanded-access": gen_form_3926,
    "expanded-access-treatment-plan": gen_treatment_plan,
    "manufacturer-letter-of-authorization": gen_loa,
    "manufacturer-loa-request": gen_loa_request,
    "irb-concurrence-request": gen_irb_request,
    "drug-accountability-log": gen_drug_accountability,
    "informed-consent-form-part50": gen_icf,
}


def generate_route_documents(study: Study, route: Dict[str, object],
                             doc_registry: Dict[str, dict]) -> Dict[str, Document]:
    """Generate every document the route declares, in the route's order.

    A doc id with no registered EA generator is skipped (its absence surfaces as
    a red 'missing document' ledger item, not a crash).
    """
    docs: Dict[str, Document] = {}
    for doc_id in route.get("documents", []):
        gen = _GENERATORS.get(doc_id)
        if gen is None:
            continue
        docs[doc_id] = gen(study, doc_registry)
    return docs
