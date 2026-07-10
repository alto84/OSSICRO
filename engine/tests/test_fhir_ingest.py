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
        self.assertRegex(coded, r"^PT-3926-[0-9A-F]{3}$")
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
