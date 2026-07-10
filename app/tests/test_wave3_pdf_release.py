"""Wave-3 app tests: the 3926 PDF/FDF export gate + the Pharma-persona release.

Covers:
  - GET /api/case/{id}/form3926.pdf and .fdf are 409 pre-commit (a draft PDF
    of an unconfirmed input must not exist) and 200 with the right headers
    and DRAFT marking once a named human committed the profile;
  - POST /api/case/{id}/release requires a committed profile AND documents
    generated from that committed input (the LOA request among them), writes
    EXACTLY ONE 'release' audit record with the hash chain intact, and
    refuses a repeat release for the same committed input;
  - an UN-released case NEVER appears in GET /api/manufacturer/inbox; a
    released case appears with the release-time snapshot and no patient
    identifiers beyond the coded id;
  - none of these endpoints ever mutates intake.

Socketless in-process requests through the REAL Handler — no port is ever
bound (the live UI-QA server on 8765 is never touched).
"""

import contextlib
import copy
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

from ossicro import audit as audit_mod                      # noqa: E402
from ossicro.review_port import DeterministicStubReviewer   # noqa: E402

ACTOR = "Jordan A. Rivera, MD"
RELEASER = "Dana Q. Osei, MD"


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
# Socketless in-process HTTP (same harness as test_wave1_hardening.py, plus a
# raw variant that returns headers + body bytes for the binary endpoints).
# ---------------------------------------------------------------------------

class _FakeSocket:
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


def _http_raw(method, path, body=None):
    """(status, {header: value}, body_bytes) through the REAL Handler."""
    payload = b"" if body is None else json.dumps(body).encode("utf-8")
    raw = ("%s %s HTTP/1.1\r\nHost: test\r\nConnection: close\r\n"
           "Content-Length: %d\r\n\r\n" % (method, path, len(payload))
           ).encode("ascii") + payload
    sock = _FakeSocket(raw)
    with contextlib.redirect_stderr(io.StringIO()):
        server.Handler(sock, ("127.0.0.1", 0), None)
    head, _, resp_body = bytes(sock.out).partition(b"\r\n\r\n")
    head_lines = head.decode("iso-8859-1").split("\r\n")
    status = int(head_lines[0].split(None, 2)[1])
    headers = {}
    for line in head_lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    return status, headers, resp_body


def _http(method, path, body=None):
    status, _headers, resp_body = _http_raw(method, path, body)
    return status, json.loads(resp_body.decode("utf-8"))


class Wave3TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-wave3-tests-")
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

    def _committed_case(self, case_id):
        case = self._register(case_id, self._sample_case())
        body, status = server._profile_commit(case, {"actor": ACTOR})
        assert status == 200, body
        return case


# ---------------------------------------------------------------------------
# form3926.pdf / .fdf — INV-3 gate + DRAFT marking
# ---------------------------------------------------------------------------

class TestForm3926Export(Wave3TestBase):

    def test_pdf_409_pre_commit(self):
        self._register("w3pdfuncommit", self._sample_case())
        status, body = _http("GET", "/api/case/w3pdfuncommit/form3926.pdf")
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "UNCOMMITTED")

    def test_fdf_409_pre_commit(self):
        self._register("w3fdfuncommit", self._sample_case())
        status, body = _http("GET", "/api/case/w3fdfuncommit/form3926.fdf")
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "UNCOMMITTED")

    def test_pdf_409_after_drift(self):
        case = self._committed_case("w3pdfdrift")
        _write_intake(case, {"patient.diagnosis": "a drifted diagnosis"})
        status, body = _http("GET", "/api/case/w3pdfdrift/form3926.pdf")
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "CONFIRMING")
        self.assertEqual(body["pending"], ["patient.diagnosis"])

    def test_fdf_409_after_drift(self):
        # MINOR-2: the FDF path is gated by require_committed, not merely
        # "a commit exists" — a drifted profile refuses the FDF too.
        case = self._committed_case("w3fdfdrift")
        _write_intake(case, {"patient.diagnosis": "a drifted diagnosis"})
        status, body = _http("GET", "/api/case/w3fdfdrift/form3926.fdf")
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "CONFIRMING")
        self.assertEqual(body["pending"], ["patient.diagnosis"])

    def test_pdf_200_committed_with_headers_and_watermark(self):
        self._committed_case("w3pdfok")
        status, headers, body = _http_raw("GET", "/api/case/w3pdfok/form3926.pdf")
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "application/pdf")
        self.assertIn("attachment", headers["content-disposition"])
        self.assertIn("DRAFT", headers["content-disposition"])
        self.assertEqual(int(headers["content-length"]), len(body))
        self.assertTrue(body.startswith(b"%PDF-"))
        self.assertIn(b"NOT FOR SUBMISSION", body)
        self.assertIn(b"Cytoravir", body)          # committed value present
        self.assertNotIn(b"[[MISSING", body)

    def test_fdf_200_committed_draft_marked(self):
        self._committed_case("w3fdfok")
        status, headers, body = _http_raw("GET", "/api/case/w3fdfok/form3926.fdf")
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "application/vnd.fdf")
        self.assertIn("attachment", headers["content-disposition"])
        self.assertTrue(body.startswith(b"%FDF-1.2"))
        self.assertIn(b"NOT FOR SUBMISSION", body)
        self.assertIn(b"/V (Cytoravir)", body)

    def test_pdf_never_mutates_intake(self):
        case = self._committed_case("w3pdfnomut")
        before = copy.deepcopy(case["intake"])
        rev_before = case["intake_rev"]
        _http_raw("GET", "/api/case/w3pdfnomut/form3926.pdf")
        _http_raw("GET", "/api/case/w3pdfnomut/form3926.fdf")
        self.assertEqual(case["intake"], before)
        self.assertEqual(case["intake_rev"], rev_before)

    def test_unknown_case_404(self):
        status, body = _http("GET", "/api/case/nosuchcase99/form3926.pdf")
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# POST /release — the named-human cross-persona SEND
# ---------------------------------------------------------------------------

class TestRelease(Wave3TestBase):

    def _generate(self, case):
        payload = server._generate_payload(case)
        self.assertTrue(payload["documents"])
        return payload

    def test_release_refused_uncommitted(self):
        self._register("w3reluncommit", self._sample_case())
        status, body = _http("POST", "/api/case/w3reluncommit/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "profile not committed")

    def test_release_refused_without_generated_loa(self):
        case = self._committed_case("w3relnogen")
        status, body = _http("POST", "/api/case/w3relnogen/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 409)
        self.assertIn("LOA request", body["error"])
        self.assertIsNone(case["released"])
        self.assertEqual([r for r in case["audit"] if r["action"] == "release"], [])

    def test_release_requires_named_actor_and_manufacturer_target(self):
        case = self._committed_case("w3relbadargs")
        self._generate(case)
        status, body = _http("POST", "/api/case/w3relbadargs/release",
                             {"actor": "   ", "to": "manufacturer"})
        self.assertEqual(status, 400)
        status, body = _http("POST", "/api/case/w3relbadargs/release",
                             {"actor": RELEASER, "to": "patient"})
        self.assertEqual(status, 400)
        self.assertIsNone(case["released"])
        self.assertEqual([r for r in case["audit"] if r["action"] == "release"], [])

    def test_release_writes_exactly_one_audit_record_chain_intact(self):
        case = self._committed_case("w3relok")
        self._generate(case)
        before_intake = copy.deepcopy(case["intake"])
        status, body = _http("POST", "/api/case/w3relok/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        self.assertEqual(body["released"]["to"], "manufacturer")
        self.assertEqual(body["released"]["actor"], RELEASER)
        self.assertEqual(body["released"]["released_hash"],
                         case["committed_profile"]["profile_hash"])
        release_recs = [r for r in case["audit"] if r["action"] == "release"]
        self.assertEqual(len(release_recs), 1)
        rec = release_recs[0]
        self.assertEqual(rec["actor"], RELEASER)
        self.assertEqual(rec["target"], "manufacturer-loa-request")
        self.assertEqual(rec["input_hash"],
                         case["committed_profile"]["profile_hash"])
        self.assertEqual(rec["detail"], {"to": "manufacturer"})
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])
        self.assertEqual(case["intake"], before_intake)   # intake untouched

    def test_repeat_release_refused_for_same_committed_input(self):
        case = self._committed_case("w3relrepeat")
        self._generate(case)
        status, _ = _http("POST", "/api/case/w3relrepeat/release",
                          {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        status, body = _http("POST", "/api/case/w3relrepeat/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 409)
        self.assertIn("already released", body["error"])
        self.assertEqual(
            len([r for r in case["audit"] if r["action"] == "release"]), 1)

    def test_re_release_after_recommit_is_a_new_named_act(self):
        case = self._committed_case("w3relagain")
        self._generate(case)
        _http("POST", "/api/case/w3relagain/release",
              {"actor": RELEASER, "to": "manufacturer"})
        # Profile changes -> reconfirm -> regenerate -> a NEW release act.
        _write_intake(case, {"drug.dose": "120 mg orally once daily"})
        body, status = server._profile_confirm(
            case, {"actor": ACTOR, "field_ids": ["drug.dose"]})
        self.assertEqual(status, 200)
        # Without regeneration the release is refused (stale artifact)...
        status, body = _http("POST", "/api/case/w3relagain/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 409)
        # ...after regeneration it is a fresh named act, audit-logged again.
        self._generate(case)
        status, body = _http("POST", "/api/case/w3relagain/release",
                             {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        self.assertEqual(
            len([r for r in case["audit"] if r["action"] == "release"]), 2)
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])


# ---------------------------------------------------------------------------
# GET /api/manufacturer/inbox — released cases only, snapshot view
# ---------------------------------------------------------------------------

class TestManufacturerInbox(Wave3TestBase):

    def test_unreleased_case_never_appears(self):
        # Committed AND generated — but never released: still invisible.
        case = self._committed_case("w3inboxhidden")
        server._generate_payload(case)
        status, body = _http("GET", "/api/manufacturer/inbox")
        self.assertEqual(status, 200)
        self.assertEqual(body["inbox"], [])   # un-released -> invisible

    def test_released_case_appears_with_coded_id_only(self):
        case = self._committed_case("w3inboxshown")
        server._generate_payload(case)
        status, _ = _http("POST", "/api/case/w3inboxshown/release",
                          {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        status, body = _http("GET", "/api/manufacturer/inbox")
        self.assertEqual(status, 200)
        self.assertEqual(len(body["inbox"]), 1)
        item = body["inbox"][0]
        # MAJOR-1: the manufacturer receives an OPAQUE release_id, never the
        # case_id (which is a full-access capability elsewhere).
        self.assertNotIn("case_id", item)
        self.assertTrue(item["release_id"])
        self.assertNotIn("w3inboxshown", json.dumps(item))
        self.assertEqual(item["patient_coded_id"], "PT-3926-014")
        self.assertEqual(item["drug"], "Cytoravir")
        self.assertIn("cholangiocarcinoma", item["indication"])
        self.assertIn("LETTER OF AUTHORIZATION", item["loa_request"])
        self.assertTrue(item["draft"])
        # No patient identifiers beyond the coded id: age/sex are not in the
        # view, and the item exposes only the fixed manufacturer-facing keys.
        item_json = json.dumps(item)
        self.assertNotIn("Female", item_json)
        self.assertNotIn("patient.age", item_json)
        self.assertEqual(
            set(item.keys()),
            {"release_id", "released_by", "released_at", "released_hash",
             "patient_coded_id", "drug", "indication", "physician",
             "loa_request", "draft"})
        # The manufacturer decision is not modeled as an OSSICRO action.
        self.assertIn("manufacturer's alone", body["note"])

    def test_inbox_shows_release_time_snapshot_not_live_intake(self):
        case = self._committed_case("w3inboxsnap")
        server._generate_payload(case)
        _http("POST", "/api/case/w3inboxsnap/release",
              {"actor": RELEASER, "to": "manufacturer"})
        # Post-release drift must NOT leak into the manufacturer view.
        _write_intake(case, {"drug.name": "UnreleasedDrugX"})
        status, body = _http("GET", "/api/manufacturer/inbox")
        item = body["inbox"][0]
        self.assertEqual(item["drug"], "Cytoravir")
        self.assertNotIn("UnreleasedDrugX", json.dumps(item))

    def test_inbox_never_mutates_intake(self):
        case = self._committed_case("w3inboxnomut")
        server._generate_payload(case)
        _http("POST", "/api/case/w3inboxnomut/release",
              {"actor": RELEASER, "to": "manufacturer"})
        before = copy.deepcopy(case["intake"])
        _http("GET", "/api/manufacturer/inbox")
        self.assertEqual(case["intake"], before)


if __name__ == "__main__":
    unittest.main()
