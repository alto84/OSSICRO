"""Wave-1 hardening tests: I-AUDIT wiring, persistence, and the m1 409 contract.

Covers:
  - each of commit / reconfirm / signoff / bundle_loaded appends EXACTLY ONE
    audit record with the right action, actor, and input_hash — and the trail
    never carries a chart value (INV-8);
  - GET /api/case/{id}/audit returns the trail;
  - inv3-review m1: the HTTP 409 {error, pending, state} contract for
    /generate and /package, driven through the REAL Handler via a socketless
    in-process request (no port is ever bound — the live UI-QA server on
    8765 is never touched);
  - inv3-review m6: POST /intake carries the profile block;
  - persistence: corruption-tolerant _load_cases, _normalize_case
    idempotency + audit backfill, and the atomic-write failure path.
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import server  # noqa: E402  (imports the engine; never binds the port)

from ossicro.review_port import DeterministicStubReviewer  # noqa: E402

ACTOR = "Jordan A. Rivera, MD"
GATE = "submission-to-fda"
DOC = "form-fda-3926-individual-patient-expanded-access"

# Distinctive synthetic chart values (they exist HERE so asserting their
# absence from the audit trail is meaningful).
DISTINCT = {"patient.coded_id": "ZQX-PATIENT-77",
            "patient.diagnosis": "XYZZY-DISTINCTIVE-DIAGNOSIS",
            "drug.name": "PLUGHVIB-999"}


def _write_intake(case, fields):
    """Mirror POST /intake's store rule (see test_commit_profile.py)."""
    before = dict(case["intake"])
    for key, value in fields.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            case["intake"].pop(key, None)
        else:
            case["intake"][key] = value
    if case["intake"] != before:
        case["intake_rev"] += 1


# ---------------------------------------------------------------------------
# Socketless in-process HTTP: drive the REAL Handler (regex routing, status
# mapping, JSON shaping) without ever binding a port.
# ---------------------------------------------------------------------------

class _FakeSocket:
    """Just enough socket for BaseHTTPRequestHandler: makefile('rb') feeds the
    raw request; sendall() captures the raw response bytes."""

    def __init__(self, request_bytes):
        self._rfile = io.BytesIO(request_bytes)
        self.out = bytearray()

    def makefile(self, mode, *args, **kwargs):
        return self._rfile

    def sendall(self, data):
        self.out += data

    def settimeout(self, value):  # pragma: no cover — defensive
        pass

    def close(self):  # pragma: no cover — defensive
        pass


def _http(method, path, body=None):
    """One in-process request through server.Handler -> (status, json_body)."""
    payload = b"" if body is None else json.dumps(body).encode("utf-8")
    raw = ("%s %s HTTP/1.1\r\nHost: test\r\nConnection: close\r\n"
           "Content-Length: %d\r\n\r\n" % (method, path, len(payload))
           ).encode("ascii") + payload
    sock = _FakeSocket(raw)
    with contextlib.redirect_stderr(io.StringIO()):   # quiet request logging
        server.Handler(sock, ("127.0.0.1", 0), None)
    head, _, resp_body = bytes(sock.out).partition(b"\r\n\r\n")
    status = int(head.split(None, 2)[1])
    return status, json.loads(resp_body.decode("utf-8"))


class Wave1TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-wave1-tests-")
        self._orig_cases_dir = server.CASES_DIR
        server.CASES_DIR = self._tmp
        self._orig_select = server._select_reviewer
        server._select_reviewer = lambda: DeterministicStubReviewer()
        self._case_ids = []

    def tearDown(self):
        for case_id in self._case_ids:
            server.CASES.pop(case_id, None)
        server.CASES_DIR = self._orig_cases_dir
        server._select_reviewer = self._orig_select
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _register(self, case_id, case=None):
        case = case if case is not None else server._new_case()
        server.CASES[case_id] = case
        self._case_ids.append(case_id)
        return case

    def _sample_case(self):
        case = server._new_case()
        _write_intake(case, server._sample_payload()["fields"])
        return case


# ---------------------------------------------------------------------------
# I-AUDIT wiring: exactly one record per act, right action, no chart values
# ---------------------------------------------------------------------------

class TestAuditWiring(Wave1TestBase):

    def test_commit_appends_exactly_one_commit_record(self):
        case = self._sample_case()
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 200)
        self.assertEqual(len(case["audit"]), 1)
        rec = case["audit"][0]
        self.assertEqual(rec["action"], "commit")
        self.assertEqual(rec["actor"], ACTOR)
        self.assertEqual(rec["seq"], 1)
        self.assertEqual(rec["input_hash"],
                         case["committed_profile"]["profile_hash"])
        self.assertIn("patient.diagnosis", rec["detail"]["field_ids"])

    def test_failed_commit_appends_nothing(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": "   "})        # 400 blank actor
        empty = server._new_case()
        server._profile_commit(empty, {"actor": ACTOR})       # 400 empty intake
        server._profile_commit(case, {"actor": ACTOR})        # 200
        _write_intake(case, {"drug.dose": "42 mg"})
        server._profile_commit(case, {"actor": ACTOR})        # 409 pending
        self.assertEqual(empty["audit"], [])
        self.assertEqual([r["action"] for r in case["audit"]], ["commit"])

    def test_confirm_appends_exactly_one_reconfirm_record(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"patient.diagnosis": "a different diagnosis"})
        body, status = server._profile_confirm(
            case, {"actor": "Casey B. Ndiaye, RN",
                   "field_ids": ["patient.diagnosis"]})
        self.assertEqual(status, 200)
        actions = [r["action"] for r in case["audit"]]
        self.assertEqual(actions, ["commit", "reconfirm"])
        rec = case["audit"][1]
        self.assertEqual(rec["actor"], "Casey B. Ndiaye, RN")
        self.assertEqual(rec["detail"]["field_ids"], ["patient.diagnosis"])
        # pending drained -> auto-recommit: the NEW committed hash is stamped
        self.assertEqual(rec["input_hash"],
                         case["committed_profile"]["profile_hash"])
        self.assertNotEqual(rec["input_hash"], case["audit"][0]["input_hash"])

    def test_failed_confirm_appends_nothing(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["drug.name"]})  # 400
        self.assertEqual([r["action"] for r in case["audit"]], ["commit"])

    def test_signoff_appends_exactly_one_record(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        record, err, status = server._record_signoff(case, {
            "gate_id": GATE, "doc_id": DOC, "signer_name": ACTOR,
            "role": "sponsor-investigator", "date": "2026-07-10"})
        self.assertIsNone(err)
        signoff_recs = [r for r in case["audit"] if r["action"] == "signoff"]
        self.assertEqual(len(signoff_recs), 1)
        rec = signoff_recs[0]
        self.assertEqual(rec["actor"], ACTOR)
        self.assertEqual(rec["target"], DOC)
        self.assertEqual(rec["detail"]["gate_id"], GATE)
        self.assertEqual(rec["detail"]["role"], "sponsor-investigator")
        # the committed-profile hash in force at signoff time
        self.assertEqual(rec["input_hash"],
                         case["committed_profile"]["profile_hash"])

    def test_failed_signoff_appends_nothing(self):
        case = self._sample_case()
        record, err, status = server._record_signoff(case, {
            "gate_id": GATE, "doc_id": DOC, "signer_name": ACTOR,
            "role": "wrong-role", "date": "2026-07-10"})
        self.assertIsNotNone(err)
        self.assertEqual(case["audit"], [])

    def test_import_appends_exactly_one_bundle_loaded_record(self):
        case_id = "auditimport1"
        case = self._register(case_id, self._sample_case())
        result, err, status = server._fhir_import(
            case, case_id, {"use_sample": True})
        self.assertIsNone(err)
        loaded = [r for r in case["audit"] if r["action"] == "bundle_loaded"]
        self.assertEqual(len(loaded), 1)
        rec = loaded[0]
        self.assertEqual(rec["actor"], "")   # honest absence: import maps only
        self.assertEqual(rec["target"], "fhir-bundle")
        self.assertTrue(rec["input_hash"].startswith("sha256:"))
        self.assertEqual(rec["detail"]["source_kind"], "sample-fixture")
        # ...and the record matches the privacy log's bundle hash
        self.assertEqual(rec["input_hash"],
                         "sha256:" + case["privacy_log"][0]["bundle_sha256"])

    def test_full_flow_trail_is_ordered_and_phi_free(self):
        case_id = "auditflow1"
        case = self._register(case_id)
        _write_intake(case, dict(DISTINCT))
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.name": "PLUGHVIB-1000"})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["drug.name"]})
        server._record_signoff(case, {
            "gate_id": GATE, "doc_id": DOC, "signer_name": ACTOR,
            "role": "sponsor-investigator", "date": "2026-07-10"})
        server._fhir_import(case, case_id, {"use_sample": True})
        self.assertEqual([r["action"] for r in case["audit"]],
                         ["commit", "reconfirm", "signoff", "bundle_loaded"])
        self.assertEqual([r["seq"] for r in case["audit"]], [1, 2, 3, 4])
        blob = json.dumps(case["audit"])
        for value in list(DISTINCT.values()) + ["PLUGHVIB-1000"]:
            self.assertNotIn(value, blob)   # INV-8: never chart values
        # the trail survives the save/load round trip intact
        server._save_case(case_id)
        server.CASES.pop(case_id)
        reloaded = server._get_case(case_id)
        self.assertEqual([r["action"] for r in reloaded["audit"]],
                         ["commit", "reconfirm", "signoff", "bundle_loaded"])

    def test_audit_endpoint_returns_the_trail(self):
        case_id = "audithttp1"
        case = self._register(case_id, self._sample_case())
        server._profile_commit(case, {"actor": ACTOR})
        status, body = _http("GET", "/api/case/%s/audit" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual([r["action"] for r in body["audit"]], ["commit"])
        self.assertEqual(body["audit"][0]["actor"], ACTOR)

    def test_audit_endpoint_unknown_case_404(self):
        status, body = _http("GET", "/api/case/nosuchcase1/audit")
        self.assertEqual(status, 404)
        self.assertIn("error", body)


# ---------------------------------------------------------------------------
# inv3-review m1 — the HTTP 409 {error, pending, state} contract, through the
# real Handler (deleting the except ProfileNotCommitted clauses fails these)
# ---------------------------------------------------------------------------

class TestHttp409Contract(Wave1TestBase):

    def test_generate_uncommitted_409_shape(self):
        case_id = "httpgen40901"
        self._register(case_id, self._sample_case())
        status, body = _http("POST", "/api/case/%s/generate" % case_id)
        self.assertEqual(status, 409)
        self.assertEqual(sorted(body), ["error", "pending", "state"])
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "UNCOMMITTED")
        self.assertEqual(body["pending"], [])

    def test_generate_drifted_409_names_pending(self):
        case_id = "httpgen40902"
        case = self._register(case_id, self._sample_case())
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.dose": "999 mg"})
        status, body = _http("POST", "/api/case/%s/generate" % case_id)
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "CONFIRMING")
        self.assertEqual(body["pending"], ["drug.dose"])

    def test_package_uncommitted_409_shape(self):
        case_id = "httppkg40901"
        self._register(case_id, self._sample_case())
        status, body = _http("GET", "/api/case/%s/package" % case_id)
        self.assertEqual(status, 409)
        self.assertEqual(sorted(body), ["error", "pending", "state"])
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "UNCOMMITTED")

    def test_generate_succeeds_200_after_commit(self):
        # the 409 mapping must not swallow the success path
        case_id = "httpgen200ok"
        case = self._register(case_id, self._sample_case())
        server._profile_commit(case, {"actor": ACTOR})
        status, body = _http("POST", "/api/case/%s/generate" % case_id)
        self.assertEqual(status, 200)
        self.assertTrue(body["documents"])


# ---------------------------------------------------------------------------
# inv3-review m6 — POST /intake carries the profile block
# ---------------------------------------------------------------------------

class TestIntakeCarriesProfile(Wave1TestBase):

    def test_intake_response_has_profile_block(self):
        case_id = "httpintake001"
        case = self._register(case_id, self._sample_case())
        server._profile_commit(case, {"actor": ACTOR})
        status, body = _http("POST", "/api/case/%s/intake" % case_id,
                             {"fields": {"drug.dose": "77 mg"},
                              "actor": ACTOR})
        self.assertEqual(status, 200)
        # COMMITTED -> CONFIRMING transition visible without a follow-up GET
        self.assertEqual(body["profile"]["state"], "CONFIRMING")
        self.assertEqual(body["profile"]["pending"], ["drug.dose"])
        # never generated -> honestly not stale (nothing exists to be stale)
        self.assertIn("stale", body)
        self.assertFalse(body["stale"])


# ---------------------------------------------------------------------------
# Persistence hardening
# ---------------------------------------------------------------------------

class TestPersistence(Wave1TestBase):

    def _write_file(self, name, text):
        with open(os.path.join(self._tmp, name), "w", encoding="utf-8") as f:
            f.write(text)

    def test_load_cases_skips_corrupt_files_and_keeps_good_ones(self):
        good = server._new_case()
        good["intake"]["patient.coded_id"] = "GOODCASE-1"
        self._write_file("goodcase0001.json", json.dumps(good))
        self._write_file("badjson00001.json", "{this is not json")
        self._write_file("notdict00001.json", "[1, 2, 3]")
        corrupt_audit = dict(server._new_case())
        corrupt_audit["audit"] = "NOT-A-LIST"
        self._write_file("badaudit0001.json", json.dumps(corrupt_audit))
        for cid in ("goodcase0001", "badjson00001", "notdict00001",
                    "badaudit0001"):
            self._case_ids.append(cid)

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            server._load_cases()          # must never crash startup

        self.assertIn("goodcase0001", server.CASES)
        self.assertEqual(server.CASES["goodcase0001"]["intake"]
                         ["patient.coded_id"], "GOODCASE-1")
        for cid in ("badjson00001", "notdict00001", "badaudit0001"):
            self.assertNotIn(cid, server.CASES)
            # the corrupt file is SKIPPED, never deleted (forensics)
            self.assertTrue(os.path.isfile(
                os.path.join(self._tmp, cid + ".json")))
        self.assertEqual(stderr.getvalue().count("skipping unreadable case"), 3)

    def test_normalize_is_idempotent_and_backfills_audit(self):
        legacy = {"generated_rev": 3, "intake": {"drug.name": "legacydrug"},
                  "intake_rev": 3, "route_id": "route-3926", "signoffs": []}
        once = server._normalize_case(json.loads(json.dumps(legacy)))
        self.assertEqual(once["audit"], [])              # backfilled
        self.assertIsNone(once["committed_profile"])     # still no auto-commit
        twice = server._normalize_case(json.loads(json.dumps(once)))
        self.assertEqual(once, twice)                    # idempotent

    def test_normalize_rejects_unrecoverable_shapes(self):
        with self.assertRaises(ValueError):
            server._normalize_case([1, 2, 3])            # non-dict case JSON
        broken = server._new_case()
        broken["audit"] = {"seq": 1}                     # trail not a list
        with self.assertRaises(ValueError):
            server._normalize_case(broken)               # never coerced to []

    def test_save_case_failure_never_clobbers_the_good_file(self):
        case_id = "atomiccase01"
        case = self._register(case_id)
        _write_intake(case, {"drug.name": "before-crash"})
        server._save_case(case_id)
        path = server._case_path(case_id)

        case["intake"]["poison"] = object()              # not JSON-serializable
        with self.assertRaises(TypeError):
            server._save_case(case_id)

        self.assertFalse(os.path.exists(path + ".tmp"))  # tmp cleaned up
        with open(path, encoding="utf-8") as f:
            on_disk = json.load(f)                       # still valid JSON
        self.assertEqual(on_disk["intake"]["drug.name"], "before-crash")
        self.assertNotIn("poison", on_disk["intake"])


class TestIntakeKeyValidation(Wave1TestBase):
    """MAJOR-1: intake rejects non-schema keys, so a PHI-shaped key can never
    reach the unremovable audit trail via the commit's field_ids."""

    def test_unknown_intake_key_rejected_and_never_audited(self):
        case_id = "intakekey0001"
        self._register(case_id)
        phi_key = "Patient John Q. Smith DOB 1980-01-01 dx pancreatic ca"
        status, body = _http("POST", "/api/case/%s/intake" % case_id,
                             {"fields": {phi_key: "yes"}})
        self.assertEqual(status, 400)
        self.assertIn("unknown", body)
        self.assertNotIn(phi_key, server.CASES[case_id]["intake"])
        self.assertEqual(server.CASES[case_id]["audit"], [])

    def test_schema_key_accepted(self):
        case_id = "intakekey0002"
        self._register(case_id)
        status, _ = _http("POST", "/api/case/%s/intake" % case_id,
                          {"fields": {"patient.age": "58"}})
        self.assertEqual(status, 200)
        self.assertEqual(server.CASES[case_id]["intake"]["patient.age"], "58")


if __name__ == "__main__":
    unittest.main(verbosity=2)
