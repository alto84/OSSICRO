"""Tests for the FHIR-ingestion subsystem (ossicro.fhir_ingest + the
POST /api/case/{id}/fhir/import endpoint).

Covers the shared-contract guarantees:
- the synthetic sample bundle yields the expected proposals with correct
  sources and confidence (17 AUTO-class extractions where the chart has data,
  plus 3 DERIVED-LOCAL suggestions);
- the never-extract list (mapping spec §1.3) is enforced: Patient.name /
  identifier / address / telecom / birthDate values can never appear in a
  proposal, and NPI never fills a license field;
- the import endpoint maps and returns proposals ONLY — case intake is never
  mutated (privacy-state-machine INV-2 / HC1);
- the parse/map path is pure and local: no network module is imported
  (INV-1).

Run: `cd engine && python -m unittest tests.test_fhir_ingest -v`.
"""

import copy
import datetime
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ossicro import fhir_ingest, routes
from ossicro.fhir_ingest import BundleError, extract_proposals

ENGINE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ENGINE_ROOT.parent
BUNDLE_PATH = ENGINE_ROOT / "fixtures" / "fhir_sample_bundle.json"

AS_OF = datetime.date(2026, 7, 9)

# Identifier strings planted in the synthetic Patient resource. None of them
# may ever appear in a proposal, a never_extracted entry, or the endpoint body.
PATIENT_IDENTIFIER_STRINGS = (
    "Fictionpatient", "Avery", "SYN-MRN-000914", "1968-03-14",
    "100 Placeholder Lane",
)
NPI_VALUE = "1234567893"


def _load_bundle():
    return json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))


def _extract(bundle=None, emergency=False):
    bundle = bundle if bundle is not None else _load_bundle()
    return extract_proposals(bundle, routes.route_for_emergency(emergency),
                             as_of=AS_OF)


class TestSampleBundleProposals(unittest.TestCase):
    """The sample bundle exercises every AUTO mapping the chart can carry."""

    @classmethod
    def setUpClass(cls):
        cls.result = _extract()
        cls.by_id = {p["field_id"]: p for p in cls.result["proposals"]}

    def test_expected_proposal_set(self):
        expected = {
            # AUTO — patient
            "patient.age", "patient.sex", "patient.diagnosis",
            "patient.prior_therapies",
            # AUTO — physician
            "investigator.name", "investigator.degrees", "investigator.address",
            "investigator.phone", "investigator.email",
            "investigator.license_number", "investigator.license_state",
            # AUTO — drug
            "drug.name", "drug.dose", "drug.route", "drug.duration",
            # AUTO — site
            "site.name",
            # DERIVED-LOCAL
            "patient.coded_id", "treatment.plan_id", "treatment.plan_version",
        }
        self.assertEqual(set(self.by_id), expected)
        self.assertEqual(len(self.result["proposals"]), 19)
        # submission.first_treatment_date: no MedicationAdministration in the
        # non-emergency sample -> unattested -> omitted (never guessed).
        self.assertNotIn("submission.first_treatment_date", self.by_id)

    def test_manual_fields_never_proposed(self):
        manual_examples = (
            "manufacturer.name", "irb.name", "waiver_10a", "waiver_10b",
            "investigator.risk_determination", "patient.no_alternative_basis",
            "treatment.monitoring_plan", "consent.risks",
            "submission.emergency_auth_datetime", "submission.fda_division",
        )
        for field_id in manual_examples:
            self.assertNotIn(field_id, self.by_id)

    def test_values_sources_confidence(self):
        by = self.by_id
        # Age: computed from birthDate at as_of; full precision -> high; the
        # birthDate itself never appears anywhere.
        self.assertEqual(by["patient.age"]["value"], "58")
        self.assertEqual(by["patient.age"]["confidence"], "high")
        self.assertEqual(by["patient.age"]["source"]["resource"], "Patient")
        # Sex: coded administrative gender, birthsex extension agrees -> high.
        self.assertEqual(by["patient.sex"]["value"], "female")
        self.assertEqual(by["patient.sex"]["confidence"], "high")
        # Diagnosis: mapper-composed narrative (dx + stage + ECOG) -> medium
        # always, with SNOMED + ICD-10-CM provenance.
        dx = by["patient.diagnosis"]
        self.assertEqual(dx["confidence"], "medium")
        self.assertIn("cholangiocarcinoma", dx["value"].lower())
        self.assertIn("Stage IV", dx["value"])
        self.assertIn("ECOG 1", dx["value"])
        self.assertIn("SNOMED CT 70179006", dx["source"]["coding"])
        self.assertIn("ICD-10-CM C22.1", dx["source"]["coding"])
        self.assertEqual(dx["source"]["resource"], "Condition")
        # Prior therapies: all four completed agents, dated, with the
        # disease-status outcome; composed prose -> medium.
        pt = by["patient.prior_therapies"]
        self.assertEqual(pt["confidence"], "medium")
        for agent in ("gemcitabine", "cisplatin", "oxaliplatin", "fluorouracil"):
            self.assertIn(agent, pt["value"])
        self.assertIn("2025-01-10", pt["value"])
        self.assertIn("Progressive disease", pt["value"])
        # The investigational candidate (draft/proposal) must NOT be listed as
        # a prior therapy.
        self.assertNotIn("Cytoravir", pt["value"])
        # Investigator: upload mode (no fhirUser) caps the section at medium.
        for field_id in ("investigator.name", "investigator.degrees",
                         "investigator.address", "investigator.phone",
                         "investigator.email", "investigator.license_number",
                         "investigator.license_state"):
            self.assertEqual(by[field_id]["confidence"], "medium", field_id)
        self.assertEqual(by["investigator.name"]["value"], "Jordan A. Rivera, MD")
        self.assertEqual(by["investigator.degrees"]["value"], "MD")
        self.assertEqual(by["investigator.phone"]["value"], "(312) 555-0148")
        self.assertEqual(by["investigator.email"]["value"],
                         "j.rivera@example-oncology.org")
        self.assertIn("4120 Cedar Parkway", by["investigator.address"]["value"])
        # License from the state-board qualification identifier — never NPI.
        self.assertEqual(by["investigator.license_number"]["value"], "036-114520")
        self.assertIn("Illinois", by["investigator.license_state"]["value"])
        # Drug: investigational agent is text-only (no RxNorm) -> medium — the
        # expected case, per mapping spec §4.
        self.assertIn("Cytoravir", by["drug.name"]["value"])
        self.assertEqual(by["drug.name"]["confidence"], "medium")
        self.assertIn(".text", by["drug.name"]["source"]["path"])
        self.assertEqual(by["drug.dose"]["value"], "240 mg")
        self.assertEqual(by["drug.dose"]["confidence"], "medium")
        # Route is SNOMED-coded -> high.
        self.assertEqual(by["drug.route"]["value"], "Oral route")
        self.assertEqual(by["drug.route"]["confidence"], "high")
        self.assertIn("SNOMED CT 26643006", by["drug.route"]["source"]["coding"])
        self.assertEqual(by["drug.duration"]["value"], "28 d")
        # Site: Encounter.serviceProvider -> Organization; medium always.
        self.assertEqual(by["site.name"]["value"], "Fictional Oncology Associates")
        self.assertEqual(by["site.name"]["confidence"], "medium")

    def test_derived_fields_local_no_chart_value(self):
        by = self.by_id
        coded = by["patient.coded_id"]["value"]
        # 8-hex suffix (MIN1): collision space widened from 4096 to ~4.3e9.
        self.assertRegex(coded, r"^PT-3926-[0-9A-F]{8}$")
        self.assertEqual(by["treatment.plan_id"]["value"],
                         "TP-CYTORAVIR-%s" % coded)
        self.assertEqual(by["treatment.plan_version"]["value"], "v1.0")
        for field_id in ("patient.coded_id", "treatment.plan_id",
                         "treatment.plan_version"):
            self.assertEqual(by[field_id]["confidence"], "low")
            self.assertEqual(by[field_id]["source"]["resource"], "(none)")
            # The pseudonym must not be built from any patient identifier.
            for s in PATIENT_IDENTIFIER_STRINGS:
                self.assertNotIn(s, by[field_id]["value"])

    def test_every_proposal_has_contract_shape(self):
        for p in self.result["proposals"]:
            self.assertEqual(
                set(p), {"field_id", "label", "value", "source", "confidence",
                         "section"})
            self.assertEqual(set(p["source"]), {"resource", "path", "coding"})
            self.assertIn(p["confidence"], ("high", "medium", "low"))
            self.assertTrue(p["label"])
            self.assertTrue(p["section"])

    def test_summary_counts(self):
        self.assertEqual(self.result["summary"],
                         {"auto": 19, "manual": 55 - 19})


class TestNeverExtract(unittest.TestCase):
    """Mapping spec §1.3 / INV-8: identifiers are structurally excluded."""

    def test_sample_bundle_output_carries_no_patient_identifier(self):
        result = _extract()
        serialized = json.dumps(result)
        for s in PATIENT_IDENTIFIER_STRINGS:
            self.assertNotIn(s, serialized)

    def test_never_extracted_reports_skipped_elements(self):
        skipped = "\n".join(_extract()["never_extracted"])
        self.assertIn("Patient.name", skipped)
        self.assertIn("Patient.identifier", skipped)
        self.assertIn("Patient.address", skipped)
        self.assertIn("Patient.birthDate", skipped)
        self.assertIn("us-npi", skipped)

    def test_npi_never_fills_license_field(self):
        result = _extract()
        for p in result["proposals"]:
            self.assertNotIn(NPI_VALUE, str(p["value"]))
        by = {p["field_id"]: p for p in result["proposals"]}
        self.assertEqual(by["investigator.license_number"]["value"],
                         "036-114520")

    def test_npi_only_practitioner_yields_no_license_proposal(self):
        bundle = _load_bundle()
        for entry in bundle["entry"]:
            res = entry["resource"]
            if res["resourceType"] == "Practitioner":
                # Strip the state-license qualification, keep the NPI-bearing
                # identifier: no license proposal may be made.
                res["qualification"] = [q for q in res["qualification"]
                                        if not q.get("identifier")]
        by = {p["field_id"]: p for p in _extract(bundle)["proposals"]}
        self.assertNotIn("investigator.license_number", by)
        self.assertNotIn("investigator.license_state", by)

    def test_minimal_patient_bundle_extracts_nothing_identifying(self):
        bundle = {
            "resourceType": "Bundle", "type": "collection",
            "entry": [{"resource": {
                "resourceType": "Patient",
                "name": [{"family": "Realname", "given": ["Xavier"]}],
                "identifier": [{"system": "urn:mrn", "value": "MRN-777001"}],
                "telecom": [{"system": "phone", "value": "(555) 010-9999"}],
                "address": [{"line": ["9 Secret St"], "city": "Anytown"}],
                "gender": "male",
                "birthDate": "1990-05-05",
            }}],
        }
        result = _extract(bundle)
        serialized = json.dumps(result)
        for leaked in ("Realname", "Xavier", "MRN-777001", "(555) 010-9999",
                       "9 Secret St", "1990-05-05"):
            self.assertNotIn(leaked, serialized)
        by = {p["field_id"]: p for p in result["proposals"]}
        # Only the de-identified facts + derived-local suggestions survive.
        self.assertEqual(by["patient.sex"]["value"], "male")
        self.assertEqual(by["patient.age"]["value"], "36")
        self.assertNotIn("patient.coded_id",
                         [s for p in result["proposals"]
                          for s in [p["value"]] if "Realname" in s])

    def test_age_90_plus_safe_harbor(self):
        bundle = _load_bundle()
        for entry in bundle["entry"]:
            if entry["resource"]["resourceType"] == "Patient":
                entry["resource"]["birthDate"] = "1930-01-01"
        by = {p["field_id"]: p for p in _extract(bundle)["proposals"]}
        self.assertEqual(by["patient.age"]["value"], "90+")

    def test_year_only_birthdate_is_medium(self):
        bundle = _load_bundle()
        for entry in bundle["entry"]:
            if entry["resource"]["resourceType"] == "Patient":
                entry["resource"]["birthDate"] = "1968"
        by = {p["field_id"]: p for p in _extract(bundle)["proposals"]}
        self.assertEqual(by["patient.age"]["confidence"], "medium")

    def test_sex_disagreement_capped_medium(self):
        bundle = _load_bundle()
        for entry in bundle["entry"]:
            res = entry["resource"]
            if res["resourceType"] == "Patient":
                res["gender"] = "male"  # now disagrees with birthsex F
        by = {p["field_id"]: p for p in _extract(bundle)["proposals"]}
        self.assertEqual(by["patient.sex"]["confidence"], "medium")
        self.assertIn("disagree", by["patient.sex"]["value"])


class TestUnattestedAndEmergency(unittest.TestCase):

    def test_absent_elements_yield_no_proposal_never_a_guess(self):
        bundle = {"resourceType": "Bundle", "type": "collection", "entry": []}
        result = _extract(bundle)
        auto = [p for p in result["proposals"]
                if p["field_id"] not in ("patient.coded_id", "treatment.plan_id",
                                         "treatment.plan_version")]
        self.assertEqual(auto, [])

    def test_first_treatment_date_from_medication_administration(self):
        bundle = _load_bundle()
        bundle["entry"].append({"resource": {
            "resourceType": "MedicationAdministration",
            "status": "completed",
            "medicationCodeableConcept": {"text": "Cytoravir (investigational)"},
            "effectiveDateTime": "2026-07-01T09:00:00-05:00",
        }})
        by = {p["field_id"]: p
              for p in _extract(bundle, emergency=True)["proposals"]}
        p = by["submission.first_treatment_date"]
        self.assertEqual(p["value"], "2026-07-01")
        self.assertEqual(p["confidence"], "medium")  # text-matched to the drug
        self.assertEqual(p["source"]["resource"], "MedicationAdministration")

    def test_non_bundle_input_raises_structured_error(self):
        with self.assertRaises(BundleError):
            extract_proposals({"resourceType": "Patient"},
                              routes.route_for_emergency(False))
        with self.assertRaises(BundleError):
            extract_proposals("not a dict",  # type: ignore[arg-type]
                              routes.route_for_emergency(False))

    def test_input_bundle_not_mutated(self):
        bundle = _load_bundle()
        before = copy.deepcopy(bundle)
        _extract(bundle)
        self.assertEqual(bundle, before)


class TestParsePurity(unittest.TestCase):
    """INV-1: the ingestion module performs no I/O and imports no network."""

    def test_no_network_imports_in_module_source(self):
        source = (ENGINE_ROOT / "ossicro" / "fhir_ingest.py").read_text(
            encoding="utf-8")
        forbidden = re.compile(
            r"^\s*(?:import|from)\s+(urllib|socket|http|requests|httplib2|aiohttp)\b",
            re.MULTILINE)
        self.assertIsNone(forbidden.search(source))

    def test_module_namespace_has_no_network_objects(self):
        for name in ("urllib", "socket", "http", "requests"):
            self.assertFalse(hasattr(fhir_ingest, name))


class TestImportEndpoint(unittest.TestCase):
    """POST /api/case/{id}/fhir/import maps and returns; intake untouched."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "ossicro_app_server", str(REPO_ROOT / "app" / "server.py"))
        cls.server_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.server_mod)
        cls.tmpdir = tempfile.mkdtemp(prefix="ossicro-fhir-test-")
        cls.server_mod.CASES_DIR = cls.tmpdir  # keep test cases out of the repo
        cls.server_mod.CASES.clear()
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), cls.server_mod.Handler)
        cls.base = "http://127.0.0.1:%d" % cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def _post(self, path, payload):
        req = urllib.request.Request(
            self.base + path, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def _get(self, path):
        with urllib.request.urlopen(self.base + path) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_import_returns_proposals_and_never_mutates_intake(self):
        _, created = self._post("/api/case", {})
        case_id = created["case_id"]

        status, body = self._post("/api/case/%s/fhir/import" % case_id,
                                  {"use_sample": True})
        self.assertEqual(status, 200)
        self.assertEqual(set(body), {"proposals", "never_extracted", "summary"})
        self.assertEqual(len(body["proposals"]), 19)
        self.assertEqual(body["summary"]["auto"], 19)
        # No patient identifier crosses the wire.
        serialized = json.dumps(body)
        for s in PATIENT_IDENTIFIER_STRINGS:
            self.assertNotIn(s, serialized)

        # THE invariant: import wrote nothing to intake (INV-2 / HC1).
        _, case = self._get("/api/case/%s" % case_id)
        self.assertEqual(case["intake"], {})
        self.assertEqual(case["intake_rev"], 0)

        # A privacy-state note was recorded (hash + metadata, never content).
        stored = self.server_mod.CASES[case_id]
        log = stored.get("privacy_log", [])
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["event"], "fhir_bundle_loaded")
        self.assertEqual(log[0]["mode"], "PREPARATORY_REVIEW")
        self.assertEqual(len(log[0]["bundle_sha256"]), 64)
        for s in PATIENT_IDENTIFIER_STRINGS:
            self.assertNotIn(s, json.dumps(log))

        # Confirmation still flows through the EXISTING intake endpoint —
        # posting a confirmed subset is what changes intake, nothing else.
        confirmed = {p["field_id"]: p["value"] for p in body["proposals"][:2]}
        status, ack = self._post("/api/case/%s/intake" % case_id,
                                 {"fields": confirmed})
        self.assertEqual(status, 200)
        self.assertEqual(ack["intake_rev"], 1)

    def test_import_with_inline_bundle(self):
        _, created = self._post("/api/case", {})
        case_id = created["case_id"]
        bundle = _load_bundle()
        status, body = self._post("/api/case/%s/fhir/import" % case_id,
                                  {"bundle": bundle})
        self.assertEqual(status, 200)
        self.assertEqual(len(body["proposals"]), 19)
        _, case = self._get("/api/case/%s" % case_id)
        self.assertEqual(case["intake"], {})

    def test_named_confirmation_persists_and_is_phi_free(self):
        # NEW-4: the named-actor + provenance substrate round-trips durably and
        # records no chart value; a no-actor POST still works (backward compat).
        _, created = self._post("/api/case", {})
        cid = created["case_id"]
        # named confirmation with chart provenance
        status, _ = self._post("/api/case/%s/intake" % cid, {
            "fields": {"patient.age": "58", "drug.name": "Cytoravir"},
            "actor": "Dr. Jordan Rivera",
            "provenance": {"patient.age": "chart-confirmed",
                           "drug.name": "chart-confirmed"}})
        self.assertEqual(status, 200)
        _, case = self._get("/api/case/%s" % cid)
        confs = case["confirmations"]
        self.assertEqual(len(confs), 1)
        self.assertEqual(confs[0]["actor"], "Dr. Jordan Rivera")
        self.assertEqual(set(confs[0]["from_chart"]), {"patient.age", "drug.name"})
        self.assertEqual(case["field_provenance"]["drug.name"], "chart-confirmed")
        # the confirmation record carries no chart value (only field ids)
        self.assertNotIn("Cytoravir", json.dumps(confs))
        # no-actor POST still writes intake and records no confirmation
        status, _ = self._post("/api/case/%s/intake" % cid,
                               {"fields": {"site.name": "Fictional Onc"}})
        self.assertEqual(status, 200)
        _, case2 = self._get("/api/case/%s" % cid)
        self.assertEqual(len(case2["confirmations"]), 1)  # unchanged
        self.assertEqual(case2["field_provenance"].get("site.name"), "manual")

    def test_bad_payloads_rejected(self):
        _, created = self._post("/api/case", {})
        case_id = created["case_id"]
        status, body = self._post("/api/case/%s/fhir/import" % case_id, {})
        self.assertEqual(status, 400)
        status, body = self._post("/api/case/%s/fhir/import" % case_id,
                                  {"bundle": {"resourceType": "Patient"}})
        self.assertEqual(status, 400)
        status, _ = self._post("/api/case/nope-nope/fhir/import",
                               {"use_sample": True})
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# Hostile-bundle battery (Phase-13 adversarial review, findings B1/B2/M1-M7).
# Each test would PASS on a broken build before the revision — they exist so a
# regression that reopens a hole fails CI. The pre-revision suite had none of
# these: deleting the leak-guard left all tests green (review finding T1).
# ---------------------------------------------------------------------------

RXNORM = fhir_ingest.RXNORM
SNOMED = fhir_ingest.SNOMED
LOINC = fhir_ingest.LOINC
CLIN = fhir_ingest.CLINICAL_STATUS_SYS
VER = fhir_ingest.VERIFICATION_STATUS_SYS


def _bundle(*resources):
    return {"resourceType": "Bundle", "type": "collection",
            "entry": [{"resource": r} for r in resources]}


def _patient(**kw):
    r = {"resourceType": "Patient"}
    r.update(kw)
    return r


def _active_condition(code):
    return {"resourceType": "Condition",
            "clinicalStatus": {"coding": [{"system": CLIN, "code": "active"}]},
            "code": code}


def _ids(result):
    return {p["field_id"]: p for p in result["proposals"]}


class TestLeakGuardHostile(unittest.TestCase):
    """B1/T1: the hardened leak-guard must actually FIRE on free-text PHI.

    Every never-extract test elsewhere plants identifiers only in structured
    Patient fields the extractors already skip. These put a patient identifier
    into FREE TEXT that reaches a proposal value — the case the guard exists
    for. Delete ``_apply_leak_guard`` and every test here fails.
    """

    def test_patient_name_in_condition_text_is_dropped(self):
        bundle = _bundle(
            _patient(name=[{"family": "Quimby", "given": ["Harriet"]}],
                     gender="female", birthDate="1968-03-14"),
            _active_condition({"text": "Metastatic cholangiocarcinoma - pt "
                                       "Harriet Quimby, MRN 88-1234"}),
        )
        result = _extract(bundle)
        self.assertNotIn("patient.diagnosis", _ids(result))
        self.assertNotIn("Quimby", json.dumps(result))
        self.assertTrue(any("leak-guard" in n and "patient.diagnosis" in n
                            for n in result["never_extracted"]))

    def test_case_mismatch_name_still_caught(self):
        # EHR stores QUIMBY/HARRIET upper-case; the note says 'Harriet Quimby'.
        bundle = _bundle(
            _patient(name=[{"family": "QUIMBY", "given": ["HARRIET"]}],
                     gender="female"),
            _active_condition({"text": "cholangiocarcinoma, patient Harriet Quimby"}),
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_birthdate_written_form_in_text_is_caught(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="male",
                     birthDate="1968-03-14"),
            _active_condition({"text": "cholangiocarcinoma, dob 3/14/1968"}),
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_no_patient_resource_text_value_fails_closed(self):
        # A draft med whose dose/name are only free text, and NO Patient to
        # check against -> the tainted values are dropped (fail closed).
        bundle = _bundle({
            "resourceType": "MedicationRequest", "status": "draft",
            "intent": "proposal",
            "medicationCodeableConcept": {"text": "Investigational agent XYZ"},
            "dosageInstruction": [{"text": "240 mg BID; counseled patient at home"}],
        })
        result = _extract(bundle)
        by = _ids(result)
        self.assertNotIn("drug.dose", by)
        self.assertNotIn("drug.name", by)
        self.assertTrue(any("could not be verified PHI-free" in n
                            for n in result["never_extracted"]))

    def test_relatedperson_name_harvested_into_basis(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "RelatedPerson",
             "name": [{"family": "Grimsby", "given": ["Ronan"]}]},
            _active_condition({"text": "cholangiocarcinoma; daughter Ronan "
                                       "Grimsby at bedside"}),
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_contained_patient_name_harvested(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "Condition",
             "clinicalStatus": {"coding": [{"system": CLIN, "code": "active"}]},
             "contained": [{"resourceType": "Patient",
                            "name": [{"family": "Hiddenname"}]}],
             "code": {"text": "cholangiocarcinoma per Hiddenname chart"}},
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_stage_observation_free_text_fails_closed(self):
        # NEW-1: PHI in a STAGE observation's free text must be dropped like
        # ECOG's is — no Patient basis -> fail closed.
        bundle = _bundle(
            _patient(gender="female"),   # no name/id -> has_basis False
            _active_condition({"coding": [{"system": SNOMED, "code": "1",
                                           "display": "Cholangiocarcinoma"}]}),
            {"resourceType": "Observation", "status": "final",
             "code": {"coding": [{"system": LOINC, "code": "21908-9"}]},
             "valueCodeableConcept": {"text": "Stage IV - per note, "
                                              "Harriet Quimby MRN 88-1234"},
             "effectiveDateTime": "2026-06-01"},
        )
        result = _extract(bundle)
        self.assertNotIn("patient.diagnosis", _ids(result))
        self.assertNotIn("Quimby", json.dumps(result))

    def test_two_char_surname_does_not_nuke_coded_term(self):
        # NEW-6: a 2-char family name must not substring-drop "Cholangiocarcinoma".
        bundle = _bundle(
            _patient(name=[{"family": "Ng"}], gender="female"),
            _active_condition({"coding": [{"system": SNOMED, "code": "1",
                                           "display": "Cholangiocarcinoma"}]}),
        )
        by = _ids(_extract(bundle))
        self.assertIn("patient.diagnosis", by)
        self.assertIn("Cholangiocarcinoma", by["patient.diagnosis"]["value"])

    def test_clean_coded_diagnosis_survives(self):
        # A coding.display (controlled terminology, no free text) is NOT tainted
        # and must pass even when the patient's name is present structurally.
        bundle = _bundle(
            _patient(name=[{"family": "Quimby"}], gender="female"),
            _active_condition({"coding": [{"system": SNOMED, "code": "70179006",
                                           "display": "Cholangiocarcinoma"}]}),
        )
        by = _ids(_extract(bundle))
        self.assertIn("patient.diagnosis", by)
        self.assertIn("Cholangiocarcinoma", by["patient.diagnosis"]["value"])


class TestSubjectScoping(unittest.TestCase):
    """NEW-5: a resource whose subject names a Patient other than the target
    belongs to someone else and must never feed this patient's proposals —
    the external-subject chimera hole. An absent subject keeps the existing
    keep-it behavior (covered throughout this file); these tests plant an
    explicit external subject."""

    _CANCER = {"coding": [{"system": SNOMED, "code": "70179006",
                           "display": "Cholangiocarcinoma"}]}

    def test_external_subject_condition_never_feeds_diagnosis(self):
        cond = _active_condition(self._CANCER)
        cond["subject"] = {"reference": "Patient/P2-external"}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            cond)
        result = _extract(bundle)
        self.assertNotIn("patient.diagnosis", _ids(result))
        self.assertNotIn("Cholangiocarcinoma", json.dumps(result))

    def test_subject_matching_target_by_local_id_is_kept(self):
        cond = _active_condition(self._CANCER)
        cond["subject"] = {"reference": "Patient/p1"}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            cond)
        self.assertIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_external_subject_observation_never_feeds_diagnosis(self):
        # The patient's own Condition is kept, but an ECOG belonging to
        # Patient/P2-external must not decorate the narrative.
        obs = {"resourceType": "Observation", "status": "final",
               "code": {"coding": [{"system": LOINC, "code": "89247-1"}]},
               "valueCodeableConcept": {"coding": [
                   {"system": SNOMED, "code": "x", "display": "ECOG 4"}]},
               "effectiveDateTime": "2026-06-01",
               "subject": {"reference": "Patient/P2-external"}}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            _active_condition(self._CANCER), obs)
        dx = _ids(_extract(bundle))["patient.diagnosis"]["value"]
        self.assertNotIn("ECOG 4", dx)

    def test_external_subject_medicationrequest_excluded(self):
        # Neither a prior therapy nor a drug candidate may come from another
        # patient's orders.
        prior = {"resourceType": "MedicationRequest", "status": "completed",
                 "intent": "order",
                 "medicationCodeableConcept": {"coding": [
                     {"system": RXNORM, "code": "12574",
                      "display": "gemcitabine"}]},
                 "subject": {"reference": "Patient/P2-external"}}
        draft = {"resourceType": "MedicationRequest", "status": "draft",
                 "intent": "proposal",
                 "medicationCodeableConcept": {"text": "Other-Pt-Agent"},
                 "subject": {"reference": "Patient/P2-external"}}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            prior, draft)
        by = _ids(_extract(bundle))
        self.assertNotIn("patient.prior_therapies", by)
        self.assertNotIn("drug.name", by)

    def test_external_subject_administration_never_dates_first_treatment(self):
        drug = {"resourceType": "MedicationRequest", "status": "draft",
                "intent": "proposal",
                "medicationCodeableConcept": {"text": "Cytoravir"}}
        ma = {"resourceType": "MedicationAdministration", "status": "completed",
              "medicationCodeableConcept": {"text": "Cytoravir"},
              "effectiveDateTime": "2026-06-15T09:00:00Z",
              "subject": {"reference": "Patient/P2-external"}}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            drug, ma)
        self.assertNotIn("submission.first_treatment_date",
                         _ids(_extract(bundle, emergency=True)))

    def test_non_patient_subject_kept(self):
        # A Group subject is out of scope for the patient filter: kept.
        cond = _active_condition(self._CANCER)
        cond["subject"] = {"reference": "Group/cohort-9"}
        bundle = _bundle(
            _patient(id="p1", name=[{"family": "Zorp"}], gender="female"),
            cond)
        self.assertIn("patient.diagnosis", _ids(_extract(bundle)))


class TestMultiPatientRefusal(unittest.TestCase):
    """M1: a multi-subject bundle is refused, not silently chimera-mapped."""

    def test_two_patients_refused(self):
        bundle = _bundle(_patient(name=[{"family": "A"}], gender="male"),
                         _patient(name=[{"family": "B"}], gender="female"))
        with self.assertRaises(BundleError):
            _extract(bundle)


class TestDrugCandidateSafety(unittest.TestCase):
    """B2: an active home-med order must never become the investigational agent."""

    def _draft(self, name, rx=None, route_code=None):
        med = ({"coding": [{"system": RXNORM, "code": rx, "display": name}]}
               if rx else {"text": name})
        di = ({"route": {"coding": [{"system": SNOMED, "code": route_code,
                                     "display": "Oral route"}]}}
              if route_code else {})
        return {"resourceType": "MedicationRequest", "status": "draft",
                "intent": "proposal", "medicationCodeableConcept": med,
                "dosageInstruction": [di] if di else []}

    def test_active_order_not_proposed_as_drug(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "MedicationRequest", "status": "active",
             "intent": "order",
             "medicationCodeableConcept": {"coding": [
                 {"system": RXNORM, "code": "29046", "display": "lisinopril"}]},
             "dosageInstruction": [{"text": "10 mg daily"}]},
            self._draft("Investigational-XYZ"),
        )
        by = _ids(_extract(bundle))
        self.assertIn("drug.name", by)
        self.assertIn("Investigational-XYZ", by["drug.name"]["value"])
        self.assertNotIn("lisinopril", json.dumps(by["drug.name"]))

    def test_only_active_order_yields_no_drug(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "MedicationRequest", "status": "active",
             "intent": "order",
             "medicationCodeableConcept": {"coding": [
                 {"system": RXNORM, "code": "29046", "display": "lisinopril"}]}},
        )
        self.assertNotIn("drug.name", _ids(_extract(bundle)))

    def test_rxnorm_candidate_capped_medium(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._draft("morphine", rx="7052"))
        self.assertEqual(_ids(_extract(bundle))["drug.name"]["confidence"], "medium")

    def _dead(self, name, status, intent="plan"):
        return {"resourceType": "MedicationRequest", "status": status,
                "intent": intent,
                "medicationCodeableConcept": {"text": name},
                "dosageInstruction": [{"route": {"coding": [
                    {"system": SNOMED, "code": "26643006", "display": "Oral route"}]}}]}

    def test_cancelled_plan_is_not_candidate(self):
        # NEW-2: a cancelled/entered-in-error/completed plan must NOT resurrect
        # as the investigational agent.
        for status in ("cancelled", "entered-in-error", "completed", "stopped"):
            bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                             self._dead("Abandoned-Agent", status))
            self.assertNotIn("drug.name", _ids(_extract(bundle)), status)

    def test_dead_plan_does_not_win_first_slot(self):
        # NEW-2: a live draft must win over a cancelled plan listed before it.
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._dead("Abandoned-Agent", "cancelled"),
            self._draft("Live-Draft"),
        )
        by = _ids(_extract(bundle))
        self.assertIn("Live-Draft", by["drug.name"]["value"])
        self.assertNotIn("Abandoned-Agent", by["drug.name"]["value"])

    def test_active_plan_remains_candidate(self):
        # Guard against over-narrowing: active+plan is still a legitimate stage.
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         {"resourceType": "MedicationRequest", "status": "active",
                          "intent": "plan",
                          "medicationCodeableConcept": {"text": "Staged-Agent"}})
        self.assertIn("drug.name", _ids(_extract(bundle)))

    def test_multiple_candidates_cap_route_and_flag(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._draft("Agent-A", route_code="26643006"),
                         self._draft("Agent-B", route_code="26643006"))
        by = _ids(_extract(bundle))
        self.assertEqual(by["drug.route"]["confidence"], "medium")  # capped
        self.assertIn("candidate", by["drug.name"]["source"]["path"])


class TestFirstTreatmentGating(unittest.TestCase):
    """M2: first_treatment_date is emergency-only, drug-scoped, whole-word."""

    def _ma(self, text):
        return {"resourceType": "MedicationAdministration", "status": "completed",
                "medicationCodeableConcept": {"text": text},
                "effectiveDateTime": "2026-06-15T09:00:00Z"}

    def _draft(self, text):
        return {"resourceType": "MedicationRequest", "status": "draft",
                "intent": "proposal", "medicationCodeableConcept": {"text": text}}

    def test_non_emergency_route_no_first_treatment(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._draft("Cytoravir"), self._ma("Cytoravir"))
        self.assertNotIn("submission.first_treatment_date",
                         _ids(_extract(bundle, emergency=False)))

    def test_emergency_no_drug_no_first_treatment(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._ma("Morphine"))  # no drug candidate at all
        self.assertNotIn("submission.first_treatment_date",
                         _ids(_extract(bundle, emergency=True)))

    def test_emergency_unrelated_admin_no_match(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._draft("Cytoravir"), self._ma("Morphine sulfate"))
        self.assertNotIn("submission.first_treatment_date",
                         _ids(_extract(bundle, emergency=True)))

    def test_shared_single_token_does_not_match(self):
        # NEW-3: "sodium chloride" admin must NOT date "sodium bicarbonate" drug
        # on the shared token "sodium" (containment, not intersection).
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"),
                         self._draft("sodium bicarbonate"),
                         self._ma("sodium chloride 0.9% injection"))
        self.assertNotIn("submission.first_treatment_date",
                         _ids(_extract(bundle, emergency=True)))

    def test_high_only_on_rxnorm_code_equality(self):
        # NEW-3: a coded candidate + coded admin with the SAME RxNorm code earns
        # high; a display-token overlap without code equality does not.
        drug = {"resourceType": "MedicationRequest", "status": "draft",
                "intent": "proposal",
                "medicationCodeableConcept": {"coding": [
                    {"system": RXNORM, "code": "999", "display": "Cytoravir"}]}}
        ma = {"resourceType": "MedicationAdministration", "status": "completed",
              "medicationCodeableConcept": {"coding": [
                  {"system": RXNORM, "code": "999", "display": "Cytoravir 50mg"}]},
              "effectiveDateTime": "2026-06-15"}
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="female"), drug, ma)
        p = _ids(_extract(bundle, emergency=True))["submission.first_treatment_date"]
        self.assertEqual(p["confidence"], "high")


class TestObservationRecency(unittest.TestCase):
    """M3: performance status reflects the most recent observation, not order."""

    def _ecog(self, text, when):
        return {"resourceType": "Observation", "status": "final",
                "code": {"coding": [{"system": LOINC, "code": "89247-1"}]},
                "valueCodeableConcept": {"coding": [
                    {"system": SNOMED, "code": "x", "display": text}]},
                "effectiveDateTime": when}

    def test_latest_ecog_wins(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            _active_condition({"coding": [{"system": SNOMED, "code": "1",
                                           "display": "Cholangiocarcinoma"}]}),
            self._ecog("ECOG 0", "2024-01-01"),   # stale, listed first
            self._ecog("ECOG 3", "2026-06-01"),   # current
        )
        dx = _ids(_extract(bundle))["patient.diagnosis"]["value"]
        self.assertIn("ECOG 3", dx)
        self.assertIn("2026-06-01", dx)
        self.assertNotIn("ECOG 0", dx)


class TestConditionStatusFiltering(unittest.TestCase):
    """M4: refuted / entered-in-error / inactive diagnoses are not proposed."""

    def test_entered_in_error_not_proposed(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "Condition",
             "verificationStatus": {"coding": [
                 {"system": VER, "code": "entered-in-error"}]},
             "code": {"coding": [{"system": SNOMED, "code": "1",
                                  "display": "Cholangiocarcinoma"}]}},
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))

    def test_inactive_condition_not_proposed(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "Condition",
             "clinicalStatus": {"coding": [{"system": CLIN, "code": "inactive"}]},
             "code": {"coding": [{"system": SNOMED, "code": "1", "display": "X"}]}},
        )
        self.assertNotIn("patient.diagnosis", _ids(_extract(bundle)))


class TestProblemListPreference(unittest.TestCase):
    """MIN2: in the non-mCODE fallback, curated problem-list-item Conditions
    with a coded (SNOMED/ICD-10-CM) diagnosis are preferred over the full
    active dump, and the narrowing is disclosed in the provenance path."""

    CAT = fhir_ingest.CONDITION_CATEGORY_SYS

    def _cond(self, code, category_code=None):
        c = _active_condition(code)
        if category_code:
            c["category"] = [{"coding": [
                {"system": self.CAT, "code": category_code}]}]
        return c

    def test_problem_list_cancer_preferred_over_encounter_diagnosis(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._cond({"coding": [{"system": SNOMED, "code": "34095006",
                                    "display": "Dehydration"}]},
                       category_code="encounter-diagnosis"),
            self._cond({"coding": [{"system": SNOMED, "code": "70179006",
                                    "display": "Cholangiocarcinoma"}]},
                       category_code="problem-list-item"),
        )
        dx = _ids(_extract(bundle))["patient.diagnosis"]
        self.assertIn("Cholangiocarcinoma", dx["value"])
        self.assertNotIn("Dehydration", dx["value"])
        self.assertIn("problem-list-item", dx["source"]["path"])

    def test_uncoded_problem_list_item_does_not_win_preference(self):
        # A text-only problem-list entry has no cancer-adjacent code system:
        # no narrowing happens, the full active list is shown.
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._cond({"coding": [{"system": SNOMED, "code": "34095006",
                                    "display": "Dehydration"}]},
                       category_code="encounter-diagnosis"),
            self._cond({"text": "metastatic biliary tract cancer"},
                       category_code="problem-list-item"),  # uncoded
        )
        dx = _ids(_extract(bundle))["patient.diagnosis"]
        self.assertIn("metastatic biliary tract cancer", dx["value"])
        self.assertIn("Dehydration", dx["value"])
        self.assertNotIn("problem-list-item", dx["source"]["path"])

    def test_no_problem_list_items_falls_back_to_full_active_list(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._cond({"coding": [{"system": SNOMED, "code": "1",
                                    "display": "Condition-A"}]}),
            self._cond({"coding": [{"system": SNOMED, "code": "2",
                                    "display": "Condition-B"}]}),
        )
        dx = _ids(_extract(bundle))["patient.diagnosis"]
        self.assertIn("Condition-A", dx["value"])
        self.assertIn("Condition-B", dx["value"])
        self.assertIn("multiple active Conditions", dx["source"]["path"])

    def test_mcode_profile_still_wins_outright(self):
        mcode = _active_condition({"coding": [
            {"system": SNOMED, "code": "70179006",
             "display": "Cholangiocarcinoma"}]})
        mcode["meta"] = {"profile": [
            "http://hl7.org/fhir/us/mcode/StructureDefinition/"
            "mcode-primary-cancer-condition"]}
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._cond({"coding": [{"system": SNOMED, "code": "34095006",
                                    "display": "Dehydration"}]},
                       category_code="problem-list-item"),
            mcode,
        )
        dx = _ids(_extract(bundle))["patient.diagnosis"]
        self.assertIn("Cholangiocarcinoma", dx["value"])
        self.assertNotIn("Dehydration", dx["value"])


class TestProvenanceAccuracy(unittest.TestCase):
    """M6/HC4: the source stamp names the element the value was read from."""

    def test_duration_from_supply_names_supply(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "MedicationRequest", "status": "draft",
             "intent": "proposal",
             "medicationCodeableConcept": {"text": "Agent-Q"},
             "dispenseRequest": {"expectedSupplyDuration": {"value": 90, "unit": "d"}}},
        )
        by = _ids(_extract(bundle))
        self.assertIn("expectedSupplyDuration", by["drug.duration"]["source"]["path"])
        self.assertNotIn("boundsDuration", by["drug.duration"]["source"]["path"])

    def test_address_fallback_names_practitioner(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            {"resourceType": "Practitioner", "name": [{"family": "Rivera"}],
             "address": [{"line": ["1 Clinic Rd"], "city": "Town"}]},
        )
        addr = _ids(_extract(bundle))["investigator.address"]["source"]
        self.assertEqual(addr["resource"], "Practitioner")
        self.assertIn("fallback", addr["path"])


class TestPractitionerSelection(unittest.TestCase):
    """MIN4: the practitioner tied to the care (Encounter.participant.
    individual, then Condition.asserter) is preferred over bundle order; the
    selection basis is disclosed; upload-mode stays capped at medium."""

    def _practitioner(self, pid, family, given):
        return {"resourceType": "Practitioner", "id": pid,
                "name": [{"family": family, "given": [given]}]}

    def test_encounter_participant_beats_bundle_order(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._practitioner("pr-first", "Coverdoc", "Casey"),   # listed first
            self._practitioner("pr-attending", "Attending", "Alex"),
            {"resourceType": "Encounter", "status": "finished",
             "participant": [{"individual":
                              {"reference": "Practitioner/pr-attending"}}]},
        )
        name = _ids(_extract(bundle))["investigator.name"]
        self.assertIn("Attending", name["value"])
        self.assertNotIn("Coverdoc", name["value"])
        self.assertIn("Encounter.participant.individual",
                      name["source"]["path"])
        self.assertEqual(name["confidence"], "medium")  # cap unchanged

    def test_condition_asserter_beats_bundle_order_when_no_encounter(self):
        cond = _active_condition({"coding": [
            {"system": SNOMED, "code": "70179006",
             "display": "Cholangiocarcinoma"}]})
        cond["asserter"] = {"reference": "Practitioner/pr-asserter"}
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._practitioner("pr-first", "Coverdoc", "Casey"),
            self._practitioner("pr-asserter", "Asserter", "Avery"),
            cond,
        )
        name = _ids(_extract(bundle))["investigator.name"]
        self.assertIn("Asserter", name["value"])
        self.assertIn("Condition.asserter", name["source"]["path"])
        self.assertEqual(name["confidence"], "medium")

    def test_fallback_to_first_practitioner_undisclosed_basis(self):
        bundle = _bundle(
            _patient(name=[{"family": "Zorp"}], gender="female"),
            self._practitioner("pr-first", "Onlydoc", "Ona"),
        )
        name = _ids(_extract(bundle))["investigator.name"]
        self.assertIn("Onlydoc", name["value"])
        self.assertNotIn("selected via", name["source"]["path"])


class TestSexUnattested(unittest.TestCase):
    """MIN3: gender 'unknown' is absence-of-fact, never a high-confidence value."""

    def test_sex_unknown_unattested(self):
        bundle = _bundle(_patient(name=[{"family": "Zorp"}], gender="unknown"))
        self.assertNotIn("patient.sex", _ids(_extract(bundle)))


class TestEngineEgressBoundary(unittest.TestCase):
    """M7/INV-4: the ingestion path egresses nothing; ``review_claude`` is the
    single sanctioned egress (the Anthropic API) and never sees chart data."""

    def test_no_outbound_client_in_engine_except_reviewer(self):
        forbidden = re.compile(
            r"^\s*(?:import|from)\s+(urllib\.request|socket|requests|httpx|"
            r"httplib2|aiohttp|http\.client)\b", re.MULTILINE)
        offenders = []
        for path in sorted((ENGINE_ROOT / "ossicro").glob("*.py")):
            if path.name == "review_claude.py":
                continue  # the one sanctioned egress (never imports the PHI path)
            if forbidden.search(path.read_text(encoding="utf-8")):
                offenders.append(path.name)
        self.assertEqual(offenders, [])

    def test_egress_module_never_imports_phi_path(self):
        src = (ENGINE_ROOT / "ossicro" / "review_claude.py").read_text(
            encoding="utf-8")
        self.assertNotIn("fhir_ingest", src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
