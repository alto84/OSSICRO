"""FHIR R4 bundle -> intake ExtractionProposals (Route-3926 EHR ingestion).

Implements the AUTO / DERIVED-LOCAL mappings of
``docs/ehr-integration/fhir-intake-mapping.md`` under the privacy state machine
of ``docs/ehr-integration/privacy-state-machine.md``:

- PURE AND LOCAL (INV-1): stdlib ``json``-shaped dicts in, plain dicts out.
  No network, no sockets, no file I/O beyond the caller-supplied bundle dict.
  This module must never import ``urllib``, ``socket``, ``http`` or any HTTP
  client (audited by test).
- PROPOSALS ONLY (INV-2 / HC1): nothing produced here is intake. The output is
  a list of ``ExtractionProposal`` dicts the physician confirms field-by-field
  in the frontend; only the existing ``POST /api/case/{id}/intake`` writes the
  input-of-record.
- SINGLE SUBJECT (INV-8, M1): a bundle carrying more than one ``Patient`` is
  refused — cross-patient contamination on a single-patient federal form is
  both a correctness and a privacy failure.
- NEVER-EXTRACT + FREE-TEXT TAINT (mapping spec §1.3, INV-8, B1): structured
  ``Patient.name`` / ``identifier`` / ``address`` / ``telecom`` and
  ``Patient.birthDate`` *as a value* are structurally excluded. Beyond that,
  any value taken from FREE TEXT (a ``.text`` element, a ``dosageInstruction``
  narrative) is treated as TAINTED: it passes through a hardened, case- and
  format-insensitive leak-guard that harvests forbidden strings from every
  Patient (including ``contained``) and ``RelatedPerson`` in the bundle and
  from birthDate in several written forms. A tainted value that cannot be
  verified against any patient basis (no Patient resource to check) is dropped
  — fail closed. Coded controlled-terminology displays (SNOMED/LOINC/RxNorm/
  ICD-10 ``coding.display``) are not free text and are not tainted. Skipped
  elements are reported in ``never_extracted`` (paths only, never values).
- UNATTESTED HONESTY (INV-6): an absent or malformed element yields NO
  proposal — never a guess, never a population prior.
- MANUAL fields (35 of 55) have no chart source and are never proposed.

Entry point:

    extract_proposals(bundle_dict, route, as_of=None)
        -> {"proposals": [...], "never_extracted": [...], "summary": {...}}

Each proposal: {field_id, label, value,
                source: {resource, path, coding}, confidence, section}.
Confidence per mapping spec §1.2: exactly coded + unambiguous = "high"; text /
inferred / mapper-composed / more-than-one-candidate = "medium"; DERIVED-LOCAL
app suggestions = "low" (no chart authority at all). In upload/paste mode (no
SMART ``fhirUser``) every ``investigator.*`` proposal is capped at "medium" —
the practitioner identity is inferred from participants (mapping spec §3). The
investigational-agent identity (``drug.name``) is capped at "medium" always:
an RxNorm-coded candidate is, if anything, *less* likely to be the
investigational agent, so a coded hit is not license to skip scrutiny (B2).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from . import routes as routes_mod

# --- coding systems ----------------------------------------------------------
SNOMED = "http://snomed.info/sct"
LOINC = "http://loinc.org"
RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
ICD10CM = "http://hl7.org/fhir/sid/icd-10-cm"
NPI_SYSTEM = "http://hl7.org/fhir/sid/us-npi"
V2_0360 = "http://terminology.hl7.org/CodeSystem/v2-0360"
BIRTHSEX_EXT = "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex"
MCODE_PRIMARY_CANCER = "mcode-primary-cancer-condition"

CLINICAL_STATUS_SYS = "http://terminology.hl7.org/CodeSystem/condition-clinical"
VERIFICATION_STATUS_SYS = "http://terminology.hl7.org/CodeSystem/condition-ver-status"

LOINC_STAGE_GROUP = "21908-9"
LOINC_ECOG = "89247-1"
LOINC_KARNOFSKY = "89243-0"
LOINC_DISEASE_STATUS = "88040-1"

# Condition statuses that quarantine a diagnosis from ever being proposed (M4):
# a refuted or mistakenly-entered diagnosis, or one no longer active, must not
# reach an FDA form. Absent status is permitted (many valid Conditions omit it).
_DEAD_CLINICAL_STATUS = frozenset({"inactive", "resolved", "remission"})
_DEAD_VERIFICATION_STATUS = frozenset({"refuted", "entered-in-error"})

# Observation statuses that count as attested results.
_FINAL_OBS_STATUS = ("final", "amended", "corrected")

# Field ids this module may EVER propose (AUTO + DERIVED-LOCAL). MANUAL fields
# are structurally impossible to propose: they are not in this whitelist.
AUTO_FIELDS = frozenset({
    "patient.age", "patient.sex", "patient.diagnosis", "patient.prior_therapies",
    "investigator.name", "investigator.degrees", "investigator.address",
    "investigator.phone", "investigator.email", "investigator.license_number",
    "investigator.license_state",
    "drug.name", "drug.dose", "drug.route", "drug.duration",
    "submission.first_treatment_date",
    "site.name",
})
DERIVED_FIELDS = frozenset({
    "patient.coded_id", "treatment.plan_id", "treatment.plan_version",
})
PROPOSABLE_FIELDS = AUTO_FIELDS | DERIVED_FIELDS

# Intake schema metadata (label/section per field id) — loaded once from the
# route registry; static app reference data, not chart content.
_FIELD_META: Dict[str, Dict[str, str]] = {
    f["id"]: {"label": f.get("label", f["id"]), "section": f.get("section", "")}
    for f in routes_mod.intake_fields()
}
TOTAL_INTAKE_FIELDS = len(_FIELD_META)

# Internal marker: a proposal whose value was taken from free text (see B1).
# Stripped from every returned proposal in the entry point.
_TAINT = "_tainted"


class BundleError(ValueError):
    """The input is not a usable FHIR Bundle. Message carries NO chart values."""


# ---------------------------------------------------------------------------
# Bundle navigation helpers (pure)
# ---------------------------------------------------------------------------

def _entries(bundle: Dict[str, Any]) -> List[Tuple[Optional[str], Dict[str, Any]]]:
    out = []
    for entry in bundle.get("entry", []) or []:
        res = entry.get("resource")
        if isinstance(res, dict) and res.get("resourceType"):
            out.append((entry.get("fullUrl"), res))
    return out


def _of_type(bundle: Dict[str, Any], resource_type: str) -> List[Dict[str, Any]]:
    return [r for _, r in _entries(bundle) if r.get("resourceType") == resource_type]


def _resolve(bundle: Dict[str, Any], reference: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Resolve an in-bundle reference by fullUrl or ResourceType/id."""
    if not isinstance(reference, dict):
        return None
    ref = reference.get("reference")
    if not ref:
        return None
    for full_url, res in _entries(bundle):
        if full_url == ref:
            return res
        rid = res.get("id")
        if rid and ref == "%s/%s" % (res.get("resourceType"), rid):
            return res
    return None


def _codings(codeable: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not isinstance(codeable, dict):
        return []
    return [c for c in codeable.get("coding", []) or [] if isinstance(c, dict)]


def _coding_in(codeable: Optional[Dict[str, Any]], system: str,
               code: Optional[str] = None) -> Optional[Dict[str, Any]]:
    for c in _codings(codeable):
        if c.get("system") == system and (code is None or c.get("code") == code):
            return c
    return None


def _coded_display(codeable: Optional[Dict[str, Any]]) -> Optional[str]:
    """First coding.display — controlled terminology, NOT free text (untainted)."""
    for c in _codings(codeable):
        if c.get("display"):
            return str(c["display"])
    return None


def _cc_value(codeable: Optional[Dict[str, Any]]) -> Tuple[Optional[str], bool]:
    """(value, tainted). Prefer the CodeableConcept.text (richer, physician-
    facing) but mark it TAINTED — free text can embed PHI and must pass the
    leak-guard. Fall back to a coding.display, which is controlled terminology
    and therefore NOT tainted.
    """
    if not isinstance(codeable, dict):
        return None, False
    if codeable.get("text"):
        return str(codeable["text"]), True          # free text -> tainted
    disp = _coded_display(codeable)
    return disp, False                                # coded display -> clean


def _coding_summary(codeable: Optional[Dict[str, Any]]) -> Optional[str]:
    """Human-readable system+code summary, e.g. 'SNOMED CT 70179006'."""
    names = {SNOMED: "SNOMED CT", LOINC: "LOINC", RXNORM: "RxNorm",
             ICD10CM: "ICD-10-CM", V2_0360: "HL7 v2-0360"}
    bits = []
    for c in _codings(codeable):
        sys_name = names.get(c.get("system"), c.get("system") or "?")
        if c.get("code"):
            bits.append("%s %s" % (sys_name, c["code"]))
    return "; ".join(bits) or None


def _has_profile(resource: Dict[str, Any], fragment: str) -> bool:
    profiles = (resource.get("meta") or {}).get("profile", []) or []
    return any(fragment in p for p in profiles)


def bundle_sha256(bundle: Dict[str, Any]) -> str:
    """Canonical hash of the bundle for the privacy log (never the content)."""
    canonical = json.dumps(bundle, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Proposal construction
# ---------------------------------------------------------------------------

def _proposal(field_id: str, value: str, resource: str, path: str,
              coding: Optional[str], confidence: str,
              tainted: bool = False) -> Dict[str, Any]:
    if field_id not in PROPOSABLE_FIELDS:
        raise AssertionError(
            "refusing to propose non-AUTO field %r (mapping spec: MANUAL fields "
            "have no chart source)" % field_id)
    meta = _FIELD_META.get(field_id, {"label": field_id, "section": ""})
    return {
        "field_id": field_id,
        "label": meta["label"],
        "value": value,
        "source": {"resource": resource, "path": path, "coding": coding},
        "confidence": confidence,
        "section": meta["section"],
        _TAINT: tainted,
    }


def _cap(confidence: str, ceiling: str) -> str:
    """Lower ``confidence`` to ``ceiling`` if it exceeds it (high>medium>low)."""
    order = {"low": 0, "medium": 1, "high": 2}
    return confidence if order.get(confidence, 1) <= order.get(ceiling, 1) else ceiling


# --- Patient section ---------------------------------------------------------

def _extract_patient(bundle, proposals, never_extracted, as_of):
    patients = _of_type(bundle, "Patient")
    if not patients:
        return
    patient = patients[0]

    # Never-extract list — record what was present and deliberately skipped.
    if patient.get("name"):
        never_extracted.append("Patient.name (never extracted — mapping spec §1.3)")
    if patient.get("identifier"):
        never_extracted.append("Patient.identifier (MRN/member ids never extracted)")
    if patient.get("address"):
        never_extracted.append("Patient.address (never extracted)")
    if patient.get("telecom"):
        never_extracted.append("Patient.telecom (never extracted)")
    if patient.get("contact"):
        never_extracted.append("Patient.contact (never extracted)")

    # patient.age — birthDate consumed here, value discarded (INV-8).
    birth = patient.get("birthDate")
    if birth:
        never_extracted.append(
            "Patient.birthDate (used only to compute age locally; the date "
            "itself is discarded and never proposed, stored, or logged)")
        age = _age_from_birthdate(str(birth), as_of) if as_of is not None else None
        if age is not None:
            value, confidence = age
            proposals.append(_proposal(
                "patient.age", value, "Patient",
                "Patient.birthDate -> age in whole years (computed locally; "
                "birthDate discarded)", None, confidence))

    # patient.sex — administrative gender, cross-checked against birthsex ext.
    # 'unknown' is the ABSENCE of a fact, not a fact: unattested, never a
    # high-confidence assertion of the string "unknown" (MIN3 / INV-6).
    gender = patient.get("gender")
    if gender in ("male", "female", "other"):
        birthsex = None
        for ext in patient.get("extension", []) or []:
            if isinstance(ext, dict) and ext.get("url") == BIRTHSEX_EXT:
                birthsex = {"F": "female", "M": "male"}.get(ext.get("valueCode"))
        if birthsex is not None and birthsex != gender:
            proposals.append(_proposal(
                "patient.sex",
                "%s (Patient.gender) / %s (us-core-birthsex extension) — "
                "sources disagree; physician must resolve" % (gender, birthsex),
                "Patient", "Patient.gender + us-core-birthsex extension",
                "FHIR administrative-gender", "medium"))
        else:
            proposals.append(_proposal(
                "patient.sex", str(gender), "Patient", "Patient.gender",
                "FHIR administrative-gender", "high"))

    # patient.diagnosis — mapper-composed narrative (dx + stage + ECOG): medium.
    _extract_diagnosis(bundle, proposals)

    # patient.prior_therapies — completed/stopped MedicationRequests: medium.
    _extract_prior_therapies(bundle, proposals)


def _age_from_birthdate(birth: str, as_of: datetime.date) -> Optional[Tuple[str, str]]:
    """(value, confidence) or None. Whole years; >=90 -> '90+' (safe harbor)."""
    birth = birth.strip()
    try:
        if len(birth) >= 10:
            bd = datetime.datetime.strptime(birth[:10], "%Y-%m-%d").date()
            confidence = "high"
        elif len(birth) == 7:
            bd = datetime.datetime.strptime(birth, "%Y-%m").date()
            confidence = "medium"
        elif len(birth) == 4:
            bd = datetime.date(int(birth), 1, 1)
            confidence = "medium"
        else:
            return None
    except ValueError:
        return None  # malformed -> unattested, never guessed (INV-6)
    years = as_of.year - bd.year - ((as_of.month, as_of.day) < (bd.month, bd.day))
    if years < 0:
        return None
    if years >= 90:
        return "90+", confidence  # 45 CFR 164.514(b)(2)(i)(C) aggregation
    return str(years), confidence


def _condition_ok(cond: Dict[str, Any]) -> bool:
    """True unless the Condition is refuted, entered-in-error, or no longer
    active (M4). Absent status is permitted."""
    ver = _coding_in(cond.get("verificationStatus"), VERIFICATION_STATUS_SYS)
    if ver is not None and ver.get("code") in _DEAD_VERIFICATION_STATUS:
        return False
    clin = _coding_in(cond.get("clinicalStatus"), CLINICAL_STATUS_SYS)
    if clin is not None and clin.get("code") in _DEAD_CLINICAL_STATUS:
        return False
    return True


def _primary_conditions(bundle) -> List[Dict[str, Any]]:
    conditions = [c for c in _of_type(bundle, "Condition") if _condition_ok(c)]
    mcode = [c for c in conditions if _has_profile(c, MCODE_PRIMARY_CANCER)]
    if mcode:
        return mcode
    active = []
    for c in conditions:
        status = _coding_in(c.get("clinicalStatus"), CLINICAL_STATUS_SYS)
        if status is not None and status.get("code") == "active":
            active.append(c)
    return active


def _extract_diagnosis(bundle, proposals):
    candidates = _primary_conditions(bundle)
    if not candidates:
        return
    parts, codings, tainted = [], [], False
    for cond in candidates:
        label, is_tainted = _cc_value(cond.get("code"))
        if not label:
            continue
        tainted = tainted or is_tainted
        summary = _coding_summary(cond.get("code"))
        parts.append("%s (%s)" % (label, summary) if summary else label)
        if summary:
            codings.append(summary)
    if not parts:
        return
    dx = " | ".join(parts) if len(parts) > 1 else parts[0]
    stage, stage_dt, stage_tainted = _latest_observation(bundle, LOINC_STAGE_GROUP)
    ecog, ecog_dt, ecog_tainted = _latest_observation(bundle, LOINC_ECOG)
    if ecog is None:
        ecog, ecog_dt, ecog_tainted = _latest_observation(bundle, LOINC_KARNOFSKY)
    tainted = tainted or stage_tainted or ecog_tainted
    bits = [dx]
    if stage:
        bits.append("Stage: %s%s" % (stage, (" (as of %s)" % stage_dt) if stage_dt else ""))
    if ecog:
        bits.append("Performance status: %s%s" % (ecog, (" (as of %s)" % ecog_dt) if ecog_dt else ""))
    note = ("multiple active Conditions — all candidates shown; "
            if len(parts) > 1 else "")
    proposals.append(_proposal(
        "patient.diagnosis", ". ".join(bits) + ".",
        "Condition",
        "Condition.code (+ Observation 21908-9 stage group, Observation "
        "89247-1 ECOG, most recent by effective date) — %smapper-composed "
        "narrative" % note,
        "; ".join(codings) or None,
        "medium", tainted=tainted))  # composed prose is medium always (§2)


def _latest_observation(bundle, loinc_code: str) -> Tuple[Optional[str], Optional[str], bool]:
    """(value_text, effective_date, tainted) for the MOST RECENT final
    Observation of ``loinc_code`` (M3: recency, not bundle order). A stale
    performance status silently overwriting a current one is a clinical
    misrepresentation; we sort by effective date descending and disclose it.
    """
    matches = []
    for obs in _of_type(bundle, "Observation"):
        if obs.get("status") not in _FINAL_OBS_STATUS:
            continue
        if _coding_in(obs.get("code"), LOINC, loinc_code) is None:
            continue
        when = obs.get("effectiveDateTime") or (obs.get("effectivePeriod") or {}).get("start")
        matches.append((str(when)[:10] if when else "", obs))
    if not matches:
        return None, None, False
    matches.sort(key=lambda kv: kv[0], reverse=True)  # ISO dates sort chronologically
    when, obs = matches[0]
    value, tainted = _cc_value(obs.get("valueCodeableConcept"))
    return value, (when or None), tainted


def _extract_prior_therapies(bundle, proposals):
    lines, codings, tainted, seen_rx = [], [], False, set()
    for mr in _of_type(bundle, "MedicationRequest"):
        if mr.get("status") not in ("completed", "stopped"):
            continue
        med = mr.get("medicationCodeableConcept")
        rx = _coding_in(med, RXNORM)
        if rx and rx.get("code"):
            if rx["code"] in seen_rx:          # de-duplicate re-orders/refills (MIN2)
                continue
            seen_rx.add(rx["code"])
            agent, agent_tainted = (rx.get("display") or rx["code"]), False
        else:
            agent, agent_tainted = _cc_value(med)
        if not agent:
            continue
        tainted = tainted or agent_tainted
        period = None
        for di in mr.get("dosageInstruction", []) or []:
            bounds = ((di.get("timing") or {}).get("repeat") or {}).get("boundsPeriod")
            if isinstance(bounds, dict) and bounds.get("start"):
                period = "%s to %s" % (bounds["start"], bounds.get("end", "?"))
                break
        if period is None and mr.get("authoredOn"):
            period = "ordered %s" % mr["authoredOn"]
        lines.append("%s (%s)" % (agent, period) if period else agent)
        summary = _coding_summary(med)
        if summary:
            codings.append(summary)
    if not lines:
        return
    value = "; ".join(lines) + "."
    outcome, outcome_dt, outcome_tainted = _latest_observation(bundle, LOINC_DISEASE_STATUS)
    if outcome:
        tainted = tainted or outcome_tainted
        value += " Documented response: %s%s." % (
            outcome, (" (%s)" % outcome_dt) if outcome_dt else "")
    proposals.append(_proposal(
        "patient.prior_therapies", value, "MedicationRequest",
        "MedicationRequest[status completed|stopped].medicationCodeableConcept "
        "(de-duplicated by RxNorm) + dosageInstruction.timing.repeat.boundsPeriod "
        "(+ Observation 88040-1 disease status) — mapper-composed narrative",
        "; ".join(codings) or None,
        "medium", tainted=tainted))  # composed prose is medium always


# --- Physician section ---------------------------------------------------------

_INVESTIGATOR_CAP_NOTE = (
    "practitioner inferred from Encounter/Condition participants "
    "(upload mode, no fhirUser) — capped at medium")


def _extract_practitioner(bundle, proposals, never_extracted):
    practitioners = _of_type(bundle, "Practitioner")
    if not practitioners:
        return
    pr = practitioners[0]

    # NPI is never a license number (mapping spec §3) and is skipped entirely.
    if any(i.get("system") == NPI_SYSTEM for i in pr.get("identifier", []) or []):
        never_extracted.append(
            "Practitioner.identifier[system=us-npi] (NPI is NOT a license "
            "number and never fills a license field)")

    # investigator.name — a practitioner's own name is not patient PHI; not tainted.
    name = _render_human_name((pr.get("name") or [None])[0])
    if name:
        proposals.append(_proposal(
            "investigator.name", name, "Practitioner",
            "Practitioner.name — " + _INVESTIGATOR_CAP_NOTE, None, "medium"))

    # investigator.degrees
    degrees, degrees_coded = [], False
    for q in pr.get("qualification", []) or []:
        coded = _coding_in(q.get("code"), V2_0360)
        if coded and coded.get("code"):
            degrees.append(coded["code"])
            degrees_coded = True
    if not degrees:
        suffix = ((pr.get("name") or [{}])[0].get("suffix") or [])
        degrees = [s for s in suffix if s]
    if degrees:
        proposals.append(_proposal(
            "investigator.degrees", ", ".join(dict.fromkeys(degrees)),
            "Practitioner",
            "Practitioner.qualification.code.coding (v2-0360)"
            if degrees_coded else "Practitioner.name.suffix",
            "HL7 v2-0360" if degrees_coded else None, "medium"))

    # PractitionerRole for this practitioner -> telecom + organization address.
    role = None
    for r in _of_type(bundle, "PractitionerRole"):
        if _resolve(bundle, r.get("practitioner")) is pr:
            role = r
            break

    # investigator.address — PractitionerRole.organization address; the
    # provenance stamp names the resource the value was actually read from (M6).
    org = _resolve(bundle, (role or {}).get("organization"))
    address = _render_address(((org or {}).get("address") or [None])[0])
    addr_resource, addr_path = "Organization", "PractitionerRole.organization -> Organization.address"
    if address is None:
        address = _render_address((pr.get("address") or [None])[0])
        addr_resource, addr_path = "Practitioner", "Practitioner.address (fallback)"
    if address:
        proposals.append(_proposal(
            "investigator.address", address, addr_resource, addr_path, None, "medium"))

    # investigator.phone / email — PractitionerRole telecom, Practitioner fallback.
    for system, field_id in (("phone", "investigator.phone"),
                             ("email", "investigator.email")):
        value, from_role = None, False
        for telecom in (role or {}).get("telecom", []) or []:
            if telecom.get("system") == system and telecom.get("value"):
                value, from_role = telecom["value"], True
                break
        if value is None:
            for telecom in pr.get("telecom", []) or []:
                if telecom.get("system") == system and telecom.get("value"):
                    value = telecom["value"]
                    break
        if value:
            proposals.append(_proposal(
                field_id, str(value),
                "PractitionerRole" if from_role else "Practitioner",
                ("PractitionerRole.telecom[%s] — " % system) + _INVESTIGATOR_CAP_NOTE
                if from_role else "Practitioner.telecom[%s] (fallback)" % system,
                None, "medium"))

    # investigator.license_number / license_state — state-board qualification
    # identifier; NPI structurally excluded. Medium at best.
    for q in pr.get("qualification", []) or []:
        for ident in q.get("identifier", []) or []:
            if ident.get("system") == NPI_SYSTEM:
                continue  # never a license number
            if not ident.get("value"):
                continue
            proposals.append(_proposal(
                "investigator.license_number", str(ident["value"]),
                "Practitioner",
                "Practitioner.qualification.identifier (state licensing board; "
                "first non-NPI qualification identifier — physician confirms)",
                None, "medium"))
            issuer = (q.get("issuer") or {}).get("display")
            if issuer:
                proposals.append(_proposal(
                    "investigator.license_state", str(issuer), "Practitioner",
                    "Practitioner.qualification.issuer.display", None, "medium"))
            return  # one license proposal; further candidates are physician's call


def _render_human_name(name: Optional[Dict[str, Any]]) -> Optional[str]:
    if not isinstance(name, dict):
        return None
    given = " ".join(name.get("given", []) or [])
    family = name.get("family") or ""
    full = (" ".join(b for b in (given, family) if b)).strip()
    suffix = ", ".join(name.get("suffix", []) or [])
    if full and suffix:
        return "%s, %s" % (full, suffix)
    return full or None


def _render_address(addr: Optional[Dict[str, Any]]) -> Optional[str]:
    if not isinstance(addr, dict):
        return None
    bits = list(addr.get("line", []) or [])
    locality = " ".join(b for b in (addr.get("city"), addr.get("state"),
                                    addr.get("postalCode")) if b)
    if locality:
        bits.append(locality)
    if addr.get("country"):
        bits.append(addr["country"])
    return ", ".join(bits) or None


# --- Drug + treatment section --------------------------------------------------

# Statuses that mean an order is closed/dead — never an EA candidate.
_CLOSED_MR_STATUSES = frozenset({"completed", "stopped", "cancelled",
                                 "entered-in-error"})


# The expanded-access candidate is a STAGED order, not an active therapy. An
# active home-med order (status=active, intent=order) is existing treatment and
# must never be mistaken for the investigational agent (B2).
def _candidate_drug_requests(bundle) -> List[Dict[str, Any]]:
    out = []
    for mr in _of_type(bundle, "MedicationRequest"):
        status = mr.get("status")
        intent = mr.get("intent")
        # A staged order (draft/on-hold), OR a plan/proposal that has NOT been
        # killed. The intent arm must still exclude dead statuses, or a
        # cancelled/entered-in-error/completed plan resurrects as the EA agent
        # (the M4 quarantine bug, re-created in the drug section — NEW-2).
        if status in ("draft", "on-hold") or (
                intent in ("proposal", "plan")
                and status not in _CLOSED_MR_STATUSES):
            out.append(mr)
    return out


def _extract_drug(bundle, proposals) -> Tuple[Optional[str], Optional[str]]:
    """Returns (drug_name, drug_rxnorm_code) — the code, when present, lets
    first_treatment match by code equality rather than a loose token overlap."""
    candidates = _candidate_drug_requests(bundle)
    if not candidates:
        return None, None
    mr = candidates[0]
    # More than one staged candidate -> the mapper cannot know which is the
    # investigational agent; cap everything drug.* at medium and say so (§1.2).
    cap = "high" if len(candidates) == 1 else "medium"
    multi_note = ("" if len(candidates) == 1 else
                  " (%d staged medication candidates in the chart — physician "
                  "must confirm which is the investigational agent)" % len(candidates))

    med = mr.get("medicationCodeableConcept")
    rx = _coding_in(med, RXNORM)
    if rx and (rx.get("display") or rx.get("code")):
        drug_name = rx.get("display") or rx.get("code")
        # drug.name is capped at MEDIUM regardless of coding: an RxNorm-coded
        # candidate is, if anything, LESS likely to be the investigational
        # agent, so a coded hit is not license to skip scrutiny (B2).
        proposals.append(_proposal(
            "drug.name", str(drug_name), "MedicationRequest",
            "MedicationRequest.medicationCodeableConcept.coding (RxNorm) — an "
            "RxNorm-coded agent is usually a marketed drug, not an "
            "investigational one; verify this is the EA candidate%s" % multi_note,
            _coding_summary(med), "medium"))
    else:
        drug_name, name_tainted = _cc_value(med)
        if drug_name:
            proposals.append(_proposal(
                "drug.name", str(drug_name), "MedicationRequest",
                "MedicationRequest.medicationCodeableConcept.text (no RxNorm "
                "code — expected for investigational agents)%s" % multi_note,
                None, "medium", tainted=name_tainted))
    if not drug_name:
        return None, None
    drug_code = rx.get("code") if rx else None

    di = (mr.get("dosageInstruction") or [{}])[0]

    # drug.dose — structured doseQuantity (clean), else dosage TEXT (tainted).
    dose_value, dose_tainted = None, False
    dose_resource_path = "MedicationRequest.dosageInstruction.doseAndRate.doseQuantity (UCUM)"
    for dr in di.get("doseAndRate", []) or []:
        dq = dr.get("doseQuantity")
        if isinstance(dq, dict) and dq.get("value") is not None:
            dose_value = ("%s %s" % (dq["value"], dq.get("unit") or dq.get("code") or "")).strip()
            break
    if dose_value is None and di.get("text"):
        dose_value, dose_tainted = str(di["text"]), True
        dose_resource_path = "MedicationRequest.dosageInstruction.text (free text)"
    if dose_value:
        proposals.append(_proposal(
            "drug.dose", dose_value, "MedicationRequest", dose_resource_path,
            "UCUM" if "doseQuantity" in dose_resource_path else None,
            "medium", tainted=dose_tainted))

    # drug.route — SNOMED-coded = high (capped by candidate ambiguity); text = medium.
    route_cc = di.get("route")
    snomed_route = _coding_in(route_cc, SNOMED)
    if snomed_route and snomed_route.get("display"):
        proposals.append(_proposal(
            "drug.route", snomed_route["display"], "MedicationRequest",
            "MedicationRequest.dosageInstruction.route.coding (SNOMED CT)",
            _coding_summary(route_cc), _cap("high", cap)))
    else:
        route_text, route_tainted = _cc_value(route_cc)
        if route_text:
            proposals.append(_proposal(
                "drug.route", route_text, "MedicationRequest",
                "MedicationRequest.dosageInstruction.route.text", None,
                "medium", tainted=route_tainted))

    # drug.duration — boundsDuration, else dispenseRequest.expectedSupplyDuration.
    # The provenance stamp names the element actually read (M6).
    duration_path = ("MedicationRequest.dosageInstruction.timing.repeat."
                     "boundsDuration (UCUM)")
    bounds = ((di.get("timing") or {}).get("repeat") or {}).get("boundsDuration")
    if not isinstance(bounds, dict):
        bounds = (mr.get("dispenseRequest") or {}).get("expectedSupplyDuration")
        duration_path = "MedicationRequest.dispenseRequest.expectedSupplyDuration (UCUM)"
    if isinstance(bounds, dict) and bounds.get("value") is not None:
        duration = ("%s %s" % (bounds["value"], bounds.get("unit") or bounds.get("code") or "")).strip()
        proposals.append(_proposal(
            "drug.duration", duration, "MedicationRequest", duration_path,
            "UCUM", "medium"))
    return str(drug_name), drug_code


def _norm_tokens(s: str) -> set:
    return set(re.sub(r"[^a-z0-9]+", " ", s.lower()).split())


def _extract_first_treatment(bundle, proposals, drug_name: Optional[str],
                             drug_code: Optional[str], emergency: bool):
    """submission.first_treatment_date — EMERGENCY-path documentation only (M2).

    Fires only when (a) the emergency route is selected, (b) a drug candidate
    was identified, and (c) a completed MedicationAdministration matches that
    agent. Matching is by RxNorm CODE EQUALITY (the only path that earns high)
    or by whole-token CONTAINMENT of one name in the other — never a single
    shared token, which would false-match "sodium chloride" to "sodium
    bicarbonate" (NEW-3).
    """
    if not emergency or not drug_name:
        return
    drug_tokens = _norm_tokens(drug_name)
    for ma in _of_type(bundle, "MedicationAdministration"):
        if ma.get("status") != "completed":
            continue
        med = ma.get("medicationCodeableConcept")
        rx = _coding_in(med, RXNORM)
        med_text = _coded_display(med) or ""
        if med_text == "" and isinstance(med, dict):
            med_text = str(med.get("text") or "")
        coded_match = bool(rx and drug_code and rx.get("code") == drug_code)
        admin_tokens = _norm_tokens(med_text)
        text_match = bool(drug_tokens and admin_tokens
                          and (drug_tokens <= admin_tokens
                               or admin_tokens <= drug_tokens))
        if not (coded_match or text_match):
            continue
        when = ma.get("effectiveDateTime") or (ma.get("effectivePeriod") or {}).get("start")
        if not when:
            continue
        proposals.append(_proposal(
            "submission.first_treatment_date", str(when)[:10],
            "MedicationAdministration",
            "MedicationAdministration[status=completed].effectiveDateTime | "
            "effectivePeriod.start (base FHIR R4; emergency route only)",
            _coding_summary(med),
            "high" if coded_match else "medium"))
        return


def _extract_site(bundle, proposals):
    for enc in _of_type(bundle, "Encounter"):
        org = _resolve(bundle, enc.get("serviceProvider"))
        if org and org.get("name"):
            proposals.append(_proposal(
                "site.name", str(org["name"]), "Encounter",
                "Encounter.serviceProvider -> Organization.name — the treatment "
                "facility may differ from the encounter site; medium always",
                None, "medium"))
            return
        for loc_entry in enc.get("location", []) or []:
            loc = _resolve(bundle, (loc_entry or {}).get("location"))
            if loc and loc.get("name"):
                proposals.append(_proposal(
                    "site.name", str(loc["name"]), "Encounter",
                    "Encounter.location -> Location.name (fallback)", None, "medium"))
                return


# --- Derived-local fields (no chart value copied) ------------------------------

def _derived_proposals(bundle, drug_name: Optional[str]) -> List[Dict[str, Any]]:
    """DERIVED-LOCAL fields: app-generated, zero chart authority -> 'low'.

    The pseudonym suffix comes from the bundle's SHA-256 (already the privacy
    log's identifier for the load event) — never from Patient.name/identifier.
    An 8-hex suffix (~4.3e9 space) keeps cross-case collision negligible in an
    EA registry (MIN1); it is per-import (a re-imported updated chart yields a
    new suffix — the app persists one per case).
    """
    suffix = bundle_sha256(bundle)[:8].upper()
    coded_id = "PT-3926-%s" % suffix
    out = [_proposal("patient.coded_id", coded_id, "(none)",
                     "generated locally (pseudonym; never from Patient.name/"
                     "identifier)", None, "low")]
    slug = None
    if drug_name:
        token = "".join(ch for ch in drug_name.split()[0] if ch.isalnum()).upper()
        slug = token or None
    plan_id = "TP-%s-%s" % (slug, coded_id) if slug else "TP-%s" % coded_id
    out.append(_proposal("treatment.plan_id", plan_id, "(none)",
                         "generated locally (local treatment-plan identifier)",
                         None, "low"))
    out.append(_proposal("treatment.plan_version", "v1.0", "(none)",
                         "generated locally (first-authorship default)",
                         None, "low"))
    return out


# ---------------------------------------------------------------------------
# Leak-guard: no proposal value may carry a patient identifier string (INV-8).
# Hardened (B1): case- and format-insensitive; harvests from every Patient
# (incl. contained) and RelatedPerson; birthDate in several written forms;
# and FAILS CLOSED on a tainted (free-text) value when there is no patient
# basis to verify against.
# ---------------------------------------------------------------------------

def _iter_all_resources(node, depth=0):
    """Yield every resource dict in the bundle, descending into contained."""
    if depth > 8 or not isinstance(node, dict):
        return
    if node.get("resourceType"):
        yield node
    for contained in node.get("contained", []) or []:
        yield from _iter_all_resources(contained, depth + 1)


def _date_variants(iso: str) -> List[str]:
    """Written forms of a YYYY-MM-DD birthDate that a note might carry."""
    try:
        d = datetime.datetime.strptime(iso[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return [iso]
    months = ["", "january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december"]
    mon = months[d.month]
    return [
        "%04d %02d %02d" % (d.year, d.month, d.day),
        "%d %d %d" % (d.month, d.day, d.year),
        "%02d %02d %04d" % (d.month, d.day, d.year),
        "%d %d %d" % (d.day, d.month, d.year),
        "%s %d %d" % (mon, d.day, d.year),
        "%d %s %d" % (d.day, mon, d.year),
    ]


def _forbidden_basis(bundle) -> Dict[str, Any]:
    """Normalized patient-identifier strings to keep out of any value.

    Returns {"subs": set(normalized distinctive substrings),
             "words": set(normalized name word-tokens),
             "has_basis": bool}. City/state are excluded (a practitioner org
    legitimately shares the patient's town).
    """
    subs, words = set(), set()

    def norm(s):
        return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()

    def add_name(name):
        if not isinstance(name, dict):
            return
        parts = list(name.get("given", []) or [])
        if name.get("family"):
            parts.append(name["family"])
        # Only MULTI-token names go to subs (substring match). Single tokens are
        # covered by the >=3-char whole-word set below — so a 2-char family name
        # cannot substring-nuke a coded term like "cholangiocarcinoma" (NEW-6).
        full = " ".join(p for p in parts if p)
        if full and " " in full:
            subs.add(norm(full))
        text = name.get("text")
        if text and " " in str(text):
            subs.add(norm(text))
        for p in parts + [text]:
            if p:
                for tok in norm(p).split():
                    if len(tok) >= 3:
                        words.add(tok)

    def norm_sub(s):
        subs.add(re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip())

    def harvest(res):
        rtype = res.get("resourceType")
        if rtype == "Patient":
            for name in res.get("name", []) or []:
                add_name(name)
            for ident in res.get("identifier", []) or []:
                if isinstance(ident, dict) and ident.get("value"):
                    norm_sub(ident["value"])
            for telecom in res.get("telecom", []) or []:
                if isinstance(telecom, dict) and telecom.get("value"):
                    norm_sub(telecom["value"])
            if res.get("birthDate"):
                for v in _date_variants(str(res["birthDate"])):
                    subs.add(v.strip())
            for addr in res.get("address", []) or []:
                if isinstance(addr, dict):
                    for line in addr.get("line", []) or []:
                        norm_sub(line)
        elif rtype == "RelatedPerson":
            for name in res.get("name", []) or []:
                add_name(name)

    # Walk every entry resource AND its contained resources (a Patient held in
    # Condition.contained still contributes to the forbidden basis — B1).
    for _, top in _entries(bundle):
        for res in _iter_all_resources(top):
            harvest(res)

    subs = {s for s in subs if len(s) >= 2}
    words = {w for w in words if len(w) >= 3}
    return {"subs": subs, "words": words, "has_basis": bool(subs or words)}


def _apply_leak_guard(bundle, proposals, never_extracted):
    basis = _forbidden_basis(bundle)
    kept = []
    for p in proposals:
        value = str(p.get("value", ""))
        norm = re.sub(r"[^a-z0-9]+", " ", value.lower())
        padded = " %s " % norm
        hit = any(s and s in norm for s in basis["subs"]) or \
            any((" %s " % w) in padded for w in basis["words"])
        # Fail closed: a free-text value we cannot verify against any patient
        # basis (no Patient/RelatedPerson in the bundle) is dropped.
        fail_closed = p.get(_TAINT) and not basis["has_basis"]
        if hit or fail_closed:
            reason = ("extracted value would carry a patient identifier"
                      if hit else
                      "free-text value could not be verified PHI-free — no "
                      "verifiable patient identifiers in the bundle to check "
                      "against; enter this field manually")
            never_extracted.append(
                "%s (proposal dropped by leak-guard: %s)" % (p["field_id"], reason))
            continue
        kept.append(p)
    return kept


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def extract_proposals(bundle_dict: Dict[str, Any], route: Dict[str, Any],
                      as_of: Optional[datetime.date] = None) -> Dict[str, Any]:
    """Map a FHIR R4 Bundle dict to ExtractionProposals. Pure and local.

    ``route`` is the selected Route-3926 variant; its ``emergency`` flag gates
    ``submission.first_treatment_date`` (M2). ``as_of`` anchors the age
    computation (the import-time date, supplied by the app layer — the engine
    itself never reads the wall clock, per the repo's time discipline). When
    ``as_of`` is None the age proposal is omitted rather than guessed.

    A bundle carrying more than one ``Patient`` is REFUSED (M1): single-patient
    expanded access requires a single-subject bundle, and mixing subjects on a
    federal form is both a correctness and a privacy failure.

    Returns {"proposals": [...], "never_extracted": [...],
             "summary": {"auto": N, "manual": M}} and never mutates its input.
    """
    if not isinstance(bundle_dict, dict) or bundle_dict.get("resourceType") != "Bundle":
        raise BundleError("input is not a FHIR R4 Bundle (expected "
                          "resourceType 'Bundle')")

    if len(_of_type(bundle_dict, "Patient")) > 1:
        raise BundleError(
            "bundle contains more than one Patient resource; single-patient "
            "expanded access requires a single-subject bundle (refused to "
            "prevent cross-patient contamination)")

    emergency = bool(route.get("emergency")) if isinstance(route, dict) else False

    proposals: List[Dict[str, Any]] = []
    never_extracted: List[str] = []

    _extract_patient(bundle_dict, proposals, never_extracted, as_of)
    _extract_practitioner(bundle_dict, proposals, never_extracted)
    drug_name, drug_code = _extract_drug(bundle_dict, proposals)
    _extract_first_treatment(bundle_dict, proposals, drug_name, drug_code, emergency)
    _extract_site(bundle_dict, proposals)
    proposals.extend(_derived_proposals(bundle_dict, drug_name))

    proposals = _apply_leak_guard(bundle_dict, proposals, never_extracted)

    # One proposal per field id (first wins — extractors already order by
    # preference); MANUAL fields are structurally absent (whitelist assert).
    # The internal taint marker is stripped here — it never leaves the module.
    seen, unique = set(), []
    for p in proposals:
        if p["field_id"] in seen:
            continue
        seen.add(p["field_id"])
        p.pop(_TAINT, None)
        unique.append(p)

    return {
        "proposals": unique,
        "never_extracted": never_extracted,
        "summary": {"auto": len(unique),
                    "manual": TOTAL_INTAKE_FIELDS - len(unique)},
    }
