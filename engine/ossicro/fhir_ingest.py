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
- NEVER-EXTRACT (mapping spec §1.3, INV-8): ``Patient.name`` / ``identifier``
  / ``address`` / ``telecom`` and ``Patient.birthDate`` *as a value* are
  structurally excluded — birthDate is consumed inside the age computation and
  discarded. NPI is never a license number. Skipped elements are reported in
  ``never_extracted`` (paths only, never values). A final leak-guard drops any
  proposal whose value would carry a patient identifier string.
- UNATTESTED HONESTY (INV-6): an absent or malformed element yields NO
  proposal — never a guess, never a population prior.
- MANUAL fields (35 of 55) have no chart source and are never proposed.

Entry point:

    extract_proposals(bundle_dict, route, as_of=None)
        -> {"proposals": [...], "never_extracted": [...], "summary": {...}}

Each proposal: {field_id, label, value,
                source: {resource, path, coding}, confidence, section}.
Confidence per mapping spec §1.2: exactly coded = "high"; text / inferred /
mapper-composed = "medium"; DERIVED-LOCAL app suggestions = "low" (no chart
authority at all). In upload/paste mode (no SMART ``fhirUser``) every
``investigator.*`` proposal is capped at "medium" — the practitioner identity
is inferred from Encounter/Condition participants (mapping spec §3).
"""

from __future__ import annotations

import datetime
import hashlib
import json
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

LOINC_STAGE_GROUP = "21908-9"
LOINC_ECOG = "89247-1"
LOINC_KARNOFSKY = "89243-0"
LOINC_DISEASE_STATUS = "88040-1"

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


def _cc_display(codeable: Optional[Dict[str, Any]]) -> Optional[str]:
    """CodeableConcept text, else first coding display."""
    if not isinstance(codeable, dict):
        return None
    if codeable.get("text"):
        return str(codeable["text"])
    for c in _codings(codeable):
        if c.get("display"):
            return str(c["display"])
    return None


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
              coding: Optional[str], confidence: str) -> Dict[str, Any]:
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
    }


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
    gender = patient.get("gender")
    if gender in ("male", "female", "other", "unknown"):
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


def _primary_conditions(bundle) -> List[Dict[str, Any]]:
    conditions = _of_type(bundle, "Condition")
    mcode = [c for c in conditions if _has_profile(c, MCODE_PRIMARY_CANCER)]
    if mcode:
        return mcode
    active = []
    for c in conditions:
        status = _coding_in(c.get("clinicalStatus"),
                            "http://terminology.hl7.org/CodeSystem/condition-clinical")
        if status is not None and status.get("code") == "active":
            active.append(c)
    return active


def _extract_diagnosis(bundle, proposals):
    candidates = _primary_conditions(bundle)
    if not candidates:
        return
    parts, codings = [], []
    for cond in candidates:
        label = _cc_display(cond.get("code"))
        if not label:
            continue
        summary = _coding_summary(cond.get("code"))
        parts.append("%s (%s)" % (label, summary) if summary else label)
        if summary:
            codings.append(summary)
    if not parts:
        return
    dx = " | ".join(parts) if len(parts) > 1 else parts[0]
    stage = _observation_value_text(bundle, LOINC_STAGE_GROUP)
    ecog = (_observation_value_text(bundle, LOINC_ECOG)
            or _observation_value_text(bundle, LOINC_KARNOFSKY))
    bits = [dx]
    if stage:
        bits.append("Stage: %s" % stage)
    if ecog:
        bits.append("Performance status: %s" % ecog)
    note = ("multiple active cancer Conditions — all candidates shown; "
            if len(parts) > 1 else "")
    proposals.append(_proposal(
        "patient.diagnosis", ". ".join(bits) + ".",
        "Condition",
        "Condition.code (+ Observation 21908-9 stage group, Observation "
        "89247-1 ECOG) — %smapper-composed narrative" % note,
        "; ".join(codings) or None,
        "medium"))  # composed prose is medium always (mapping spec §2)


def _observation_value_text(bundle, loinc_code: str) -> Optional[str]:
    for obs in _of_type(bundle, "Observation"):
        if obs.get("status") not in ("final", "amended", "corrected"):
            continue
        if _coding_in(obs.get("code"), LOINC, loinc_code) is None:
            continue
        return _cc_display(obs.get("valueCodeableConcept"))
    return None


def _extract_prior_therapies(bundle, proposals):
    lines, codings = [], []
    for mr in _of_type(bundle, "MedicationRequest"):
        if mr.get("status") not in ("completed", "stopped"):
            continue
        med = mr.get("medicationCodeableConcept")
        rx = _coding_in(med, RXNORM)
        agent = (rx.get("display") if rx and rx.get("display") else _cc_display(med))
        if not agent:
            continue
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
    outcome = None
    for obs in _of_type(bundle, "Observation"):
        if (_coding_in(obs.get("code"), LOINC, LOINC_DISEASE_STATUS) is not None
                and obs.get("status") in ("final", "amended", "corrected")):
            outcome = _cc_display(obs.get("valueCodeableConcept"))
            when = obs.get("effectiveDateTime")
            if outcome and when:
                outcome = "%s (%s)" % (outcome, str(when)[:10])
            break
    if outcome:
        value += " Documented response: %s." % outcome
    proposals.append(_proposal(
        "patient.prior_therapies", value, "MedicationRequest",
        "MedicationRequest[status completed|stopped].medicationCodeableConcept "
        "+ dosageInstruction.timing.repeat.boundsPeriod (+ Observation 88040-1 "
        "disease status) — mapper-composed narrative",
        "; ".join(codings) or None,
        "medium"))  # composed prose is medium always


# --- Physician section ---------------------------------------------------------

_INVESTIGATOR_CAP_NOTE = (
    "practitioner inferred from Encounter/Condition participants "
    "(upload mode, no fhirUser) — capped at medium")


def _cap_medium(confidence: str) -> str:
    return "medium" if confidence == "high" else confidence


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

    # investigator.name
    name = _render_human_name((pr.get("name") or [None])[0])
    if name:
        proposals.append(_proposal(
            "investigator.name", name, "Practitioner",
            "Practitioner.name — " + _INVESTIGATOR_CAP_NOTE, None,
            _cap_medium("high")))

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
            "HL7 v2-0360" if degrees_coded else None,
            _cap_medium("high" if degrees_coded else "medium")))

    # PractitionerRole for this practitioner -> telecom + organization address.
    role = None
    for r in _of_type(bundle, "PractitionerRole"):
        if _resolve(bundle, r.get("practitioner")) is pr:
            role = r
            break

    # investigator.address — PractitionerRole.organization address; medium always.
    org = _resolve(bundle, (role or {}).get("organization"))
    address = _render_address(((org or {}).get("address") or [None])[0])
    addr_path = "PractitionerRole.organization -> Organization.address"
    if address is None:
        address = _render_address((pr.get("address") or [None])[0])
        addr_path = "Practitioner.address (fallback)"
    if address:
        proposals.append(_proposal(
            "investigator.address", address,
            "Organization" if org else "Practitioner", addr_path, None, "medium"))

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
                None,
                _cap_medium("high" if from_role else "medium")))

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
                "Practitioner.qualification.identifier (state licensing board)",
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

_CLOSED_MR_STATUSES = ("completed", "stopped", "cancelled", "entered-in-error")


def _candidate_drug_request(bundle) -> Optional[Dict[str, Any]]:
    """The staged/proposed investigational-agent MedicationRequest, if any.

    Prior therapies are completed/stopped; the expanded-access candidate is the
    open request (intent proposal|plan|order|original-order, status not closed).
    """
    for mr in _of_type(bundle, "MedicationRequest"):
        if mr.get("status") in _CLOSED_MR_STATUSES:
            continue
        if mr.get("intent") in ("proposal", "plan", "order", "original-order"):
            return mr
    return None


def _extract_drug(bundle, proposals) -> Optional[str]:
    mr = _candidate_drug_request(bundle)
    if mr is None:
        return None
    med = mr.get("medicationCodeableConcept")
    rx = _coding_in(med, RXNORM)
    if rx and (rx.get("display") or rx.get("code")):
        drug_name = rx.get("display") or rx.get("code")
        proposals.append(_proposal(
            "drug.name", str(drug_name), "MedicationRequest",
            "MedicationRequest.medicationCodeableConcept.coding (RxNorm)",
            _coding_summary(med), "high"))
    else:
        drug_name = _cc_display(med)
        if drug_name:
            proposals.append(_proposal(
                "drug.name", str(drug_name), "MedicationRequest",
                "MedicationRequest.medicationCodeableConcept.text (no RxNorm "
                "code — expected for investigational agents)", None, "medium"))
    if not drug_name:
        return None

    di = (mr.get("dosageInstruction") or [{}])[0]

    # drug.dose — structured doseQuantity, else dosage text. Medium always.
    dose_value = None
    for dr in di.get("doseAndRate", []) or []:
        dq = dr.get("doseQuantity")
        if isinstance(dq, dict) and dq.get("value") is not None:
            dose_value = ("%s %s" % (dq["value"], dq.get("unit") or dq.get("code") or "")).strip()
            break
    dose_path = "MedicationRequest.dosageInstruction.doseAndRate.doseQuantity (UCUM)"
    if dose_value is None and di.get("text"):
        dose_value, dose_path = str(di["text"]), "MedicationRequest.dosageInstruction.text"
    if dose_value:
        proposals.append(_proposal(
            "drug.dose", dose_value, "MedicationRequest", dose_path,
            "UCUM" if "doseQuantity" in dose_path else None, "medium"))

    # drug.route — SNOMED-coded = high; text = medium.
    route_cc = di.get("route")
    snomed_route = _coding_in(route_cc, SNOMED)
    if snomed_route and snomed_route.get("display"):
        proposals.append(_proposal(
            "drug.route", snomed_route["display"], "MedicationRequest",
            "MedicationRequest.dosageInstruction.route.coding (SNOMED CT)",
            _coding_summary(route_cc), "high"))
    else:
        route_text = _cc_display(route_cc)
        if route_text:
            proposals.append(_proposal(
                "drug.route", route_text, "MedicationRequest",
                "MedicationRequest.dosageInstruction.route.text", None, "medium"))

    # drug.duration — boundsDuration / expectedSupplyDuration. Medium always.
    bounds = ((di.get("timing") or {}).get("repeat") or {}).get("boundsDuration")
    if not isinstance(bounds, dict):
        bounds = (mr.get("dispenseRequest") or {}).get("expectedSupplyDuration")
    if isinstance(bounds, dict) and bounds.get("value") is not None:
        duration = ("%s %s" % (bounds["value"], bounds.get("unit") or bounds.get("code") or "")).strip()
        proposals.append(_proposal(
            "drug.duration", duration, "MedicationRequest",
            "MedicationRequest.dosageInstruction.timing.repeat.boundsDuration "
            "(UCUM)", "UCUM", "medium"))
    return str(drug_name)


def _extract_first_treatment(bundle, proposals, drug_name: Optional[str]):
    """submission.first_treatment_date — emergency-path documentation only.

    Fires only when a completed MedicationAdministration for the agent exists
    (base FHIR R4; not a US Core profile). Absent = unattested = no proposal
    (correct in the non-emergency path).
    """
    for ma in _of_type(bundle, "MedicationAdministration"):
        if ma.get("status") != "completed":
            continue
        med = ma.get("medicationCodeableConcept")
        rx = _coding_in(med, RXNORM)
        med_text = _cc_display(med) or ""
        coded_match = bool(rx and drug_name and rx.get("display") == drug_name)
        text_match = bool(drug_name and med_text
                          and drug_name.split()[0].lower() in med_text.lower())
        if drug_name and not (coded_match or text_match):
            continue
        when = ma.get("effectiveDateTime") or (ma.get("effectivePeriod") or {}).get("start")
        if not when:
            continue
        proposals.append(_proposal(
            "submission.first_treatment_date", str(when)[:10],
            "MedicationAdministration",
            "MedicationAdministration[status=completed].effectiveDateTime | "
            "effectivePeriod.start (base FHIR R4)",
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
    """
    suffix = bundle_sha256(bundle)[:3].upper()
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
# Leak-guard: no proposal value may carry a patient identifier string (INV-8)
# ---------------------------------------------------------------------------

def _patient_forbidden_strings(bundle) -> List[str]:
    """High-risk identifier strings from Patient resources.

    City/state are deliberately not included (a practitioner org legitimately
    shares the patient's town); names, identifier values, telecom values,
    birthDate, and street lines are unambiguous leaks.
    """
    forbidden: List[str] = []
    for patient in _of_type(bundle, "Patient"):
        for name in patient.get("name", []) or []:
            if not isinstance(name, dict):
                continue
            for part in ([name.get("family"), name.get("text")]
                         + list(name.get("given", []) or [])):
                if part:
                    forbidden.append(str(part))
        for ident in patient.get("identifier", []) or []:
            if isinstance(ident, dict) and ident.get("value"):
                forbidden.append(str(ident["value"]))
        for telecom in patient.get("telecom", []) or []:
            if isinstance(telecom, dict) and telecom.get("value"):
                forbidden.append(str(telecom["value"]))
        if patient.get("birthDate"):
            forbidden.append(str(patient["birthDate"]))
        for addr in patient.get("address", []) or []:
            if isinstance(addr, dict):
                forbidden.extend(str(line) for line in addr.get("line", []) or [])
    return [f for f in forbidden if len(f) >= 2]


def _apply_leak_guard(bundle, proposals, never_extracted):
    forbidden = _patient_forbidden_strings(bundle)
    if not forbidden:
        return proposals
    kept = []
    for p in proposals:
        value = str(p.get("value", ""))
        if any(f in value for f in forbidden):
            # Report the FIELD, never the value (INV-8).
            never_extracted.append(
                "%s (proposal dropped by leak-guard: extracted value would "
                "carry a patient identifier)" % p["field_id"])
            continue
        kept.append(p)
    return kept


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def extract_proposals(bundle_dict: Dict[str, Any], route: Dict[str, Any],
                      as_of: Optional[datetime.date] = None) -> Dict[str, Any]:
    """Map a FHIR R4 Bundle dict to ExtractionProposals. Pure and local.

    ``route`` is the selected Route-3926 variant (emergency vs non-emergency);
    it scopes nothing destructive — the emergency-only conditional field simply
    has no source resource in the non-emergency path. ``as_of`` anchors the age
    computation (the import-time date, supplied by the app layer — the engine
    itself never reads the wall clock, per the repo's time discipline). When
    ``as_of`` is None the age proposal is omitted rather than guessed.

    Returns {"proposals": [...], "never_extracted": [...],
             "summary": {"auto": N, "manual": M}} and never mutates its input.
    """
    if not isinstance(bundle_dict, dict) or bundle_dict.get("resourceType") != "Bundle":
        raise BundleError("input is not a FHIR R4 Bundle (expected "
                          "resourceType 'Bundle')")

    proposals: List[Dict[str, Any]] = []
    never_extracted: List[str] = []

    _extract_patient(bundle_dict, proposals, never_extracted, as_of)
    _extract_practitioner(bundle_dict, proposals, never_extracted)
    drug_name = _extract_drug(bundle_dict, proposals)
    _extract_first_treatment(bundle_dict, proposals, drug_name)
    _extract_site(bundle_dict, proposals)
    proposals.extend(_derived_proposals(bundle_dict, drug_name))

    proposals = _apply_leak_guard(bundle_dict, proposals, never_extracted)

    # One proposal per field id (first wins — extractors already order by
    # preference); MANUAL fields are structurally absent (whitelist assert).
    seen, unique = set(), []
    for p in proposals:
        if p["field_id"] in seen:
            continue
        seen.add(p["field_id"])
        unique.append(p)

    return {
        "proposals": unique,
        "never_extracted": never_extracted,
        "summary": {"auto": len(unique),
                    "manual": TOTAL_INTAKE_FIELDS - len(unique)},
    }
