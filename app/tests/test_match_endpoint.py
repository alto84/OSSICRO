"""App-level tests for POST /api/case/{id}/match (Wave 2, features B+C).

Drives the REAL Handler via a socketless in-process request (the same
harness as test_wave1_hardening — no port is ever bound; the live UI-QA
server on 8765 is never touched). Covers:

- the INV-3 gate: 409 {error:'profile not committed', pending, state} before
  a named-human commit — the same require_committed rule as /generate;
- committed profile -> 200 with the shared /match contract shape and
  candidates for the synthetic cholangiocarcinoma sample case;
- NO score/confidence key anywhere in the response; criteria lists only;
- the response's predicates carry no names / dates / free text from intake;
- the endpoint NEVER mutates intake (intake and intake_rev are byte-stable);
- every registry query wrote an 'egress_query' audit record, persisted, with
  an intact hash chain.
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

from ossicro import audit as audit_mod                      # noqa: E402
from ossicro.review_port import DeterministicStubReviewer   # noqa: E402

ACTOR = "Jordan A. Rivera, MD"

# Strings that exist in the sample intake and must NEVER cross into the
# /match response (the de-identified predicates carry codes/bands only).
INTAKE_ONLY_STRINGS = ("Jordan A. Rivera", "555-0148", "Rivertown",
                       "PT-3926-014", "2026-06-15", "Refractory metastatic")


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


def _http(method, path, body=None):
    payload = b"" if body is None else json.dumps(body).encode("utf-8")
    raw = ("%s %s HTTP/1.1\r\nHost: test\r\nConnection: close\r\n"
           "Content-Length: %d\r\n\r\n" % (method, path, len(payload))
           ).encode("ascii") + payload
    sock = _FakeSocket(raw)
    with contextlib.redirect_stderr(io.StringIO()):
        server.Handler(sock, ("127.0.0.1", 0), None)
    head, _, resp_body = bytes(sock.out).partition(b"\r\n\r\n")
    status = int(head.split(None, 2)[1])
    return status, json.loads(resp_body.decode("utf-8"))


class MatchEndpointTestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-match-tests-")
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

    def _new_case(self):
        status, body = _http("POST", "/api/case")
        self.assertEqual(status, 200)
        self._case_ids.append(body["case_id"])
        return body["case_id"]

    def _committed_sample_case(self):
        case_id = self._new_case()
        # The sample fixture carries a couple of accountability-log fields
        # that are not in the Route-3926 intake schema; POST /intake rightly
        # rejects unknown ids, so send the schema subset (as the UI would).
        fields = {k: v for k, v in server._sample_payload()["fields"].items()
                  if k in server.SCHEMA_FIELDS}
        status, _ = _http("POST", "/api/case/%s/intake" % case_id,
                          {"fields": fields, "actor": ACTOR})
        self.assertEqual(status, 200)
        status, body = _http("POST", "/api/case/%s/profile/commit" % case_id,
                             {"actor": ACTOR})
        self.assertEqual(status, 200)
        self.assertEqual(body["profile"]["state"], "COMMITTED")
        return case_id


class TestMatchGate(MatchEndpointTestBase):

    def test_409_before_commit(self):
        case_id = self._new_case()
        status, body = _http("POST", "/api/case/%s/match" % case_id)
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "UNCOMMITTED")
        self.assertIn("pending", body)
        # The refusal wrote nothing: no egress happened, no audit record.
        self.assertEqual(server.CASES[case_id]["audit"], [])

    def test_409_when_drifted_from_commit(self):
        case_id = self._committed_sample_case()
        # Mutate one confirmed field: matching must refuse like /generate does.
        status, _ = _http("POST", "/api/case/%s/intake" % case_id,
                          {"fields": {"patient.age": "61"}, "actor": ACTOR})
        self.assertEqual(status, 200)
        status, body = _http("POST", "/api/case/%s/match" % case_id)
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "CONFIRMING")
        self.assertIn("patient.age", body["pending"])

    def test_unknown_case_404(self):
        status, body = _http("POST", "/api/case/nope-nope-nope/match")
        self.assertEqual(status, 404)


class TestMatchContract(MatchEndpointTestBase):

    def test_committed_case_yields_candidates(self):
        case_id = self._committed_sample_case()
        status, body = _http("POST", "/api/case/%s/match" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(set(body),
                         {"candidates", "absence", "absence_message",
                          "queried_registries", "predicates_used", "as_of"})
        self.assertFalse(body["absence"])
        ids = {c["id"] for c in body["candidates"]}
        # The synthetic cholangiocarcinoma sample matches the fixture trials
        # and both expanded-access records.
        self.assertIn("NCT90000001", ids)
        self.assertIn("EA-90000001", ids)
        for c in body["candidates"]:
            self.assertIn(c["kind"], ("trial", "ea_record"))
            self.assertEqual(set(c), {"kind", "id", "title", "source_registry",
                                      "source_url", "matched_criteria",
                                      "unmatched_criteria",
                                      "unverifiable_criteria"})
        # Predicates used: the de-identified closed set, band not raw age.
        used = body["predicates_used"]
        self.assertEqual(used["age_band"], "55-59")
        self.assertEqual(used["sex"], "female")
        # Investigational agent -> None; raw drug text never egresses (MAJOR-2).
        self.assertIsNone(used["drug"])
        self.assertIn("C22.1", used["condition_codes"])

    def test_no_score_and_no_intake_leak_in_response(self):
        case_id = self._committed_sample_case()
        _, body = _http("POST", "/api/case/%s/match" % case_id)
        serialized = json.dumps(body)
        for banned in ('"score"', "confidence", '"ranking"'):
            self.assertNotIn(banned, serialized.lower())
        for s in INTAKE_ONLY_STRINGS:
            self.assertNotIn(s, serialized)

    def test_endpoint_never_mutates_intake(self):
        case_id = self._committed_sample_case()
        _, before = _http("GET", "/api/case/%s" % case_id)
        status, _ = _http("POST", "/api/case/%s/match" % case_id)
        self.assertEqual(status, 200)
        _, after = _http("GET", "/api/case/%s" % case_id)
        self.assertEqual(after["intake"], before["intake"])
        self.assertEqual(after["intake_rev"], before["intake_rev"])
        self.assertEqual(after["profile"]["state"], "COMMITTED")
        self.assertEqual(after["profile"]["profile_hash"],
                         before["profile"]["profile_hash"])

    def test_match_audit_logged_and_persisted(self):
        case_id = self._committed_sample_case()
        _, match_body = _http("POST", "/api/case/%s/match" % case_id)
        status, body = _http("GET", "/api/case/%s/audit" % case_id)
        self.assertEqual(status, 200)
        egress_records = [r for r in body["audit"]
                          if r["action"] == "egress_query"]
        self.assertEqual(sorted(r["target"] for r in egress_records),
                         match_body["queried_registries"])
        self.assertTrue(body["chain_ok"])
        # The audit trail is value-free: no intake strings, and the withheld
        # local filters are named, not valued.
        serialized = json.dumps(egress_records)
        for s in INTAKE_ONLY_STRINGS:
            self.assertNotIn(s, serialized)
        self.assertNotIn("55-59", serialized)   # age band never egressed
        # Persisted: reload from disk and re-verify the chain.
        path = os.path.join(server.CASES_DIR, case_id + ".json")
        with open(path, encoding="utf-8") as f:
            on_disk = json.load(f)
        self.assertEqual(audit_mod.verify_chain(on_disk["audit"]), [])
        self.assertTrue(any(r["action"] == "egress_query"
                            for r in on_disk["audit"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
