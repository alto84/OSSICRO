"""Overhaul P4 — app-side tests: the manufacturer concern end-to-end.

Covers:
  - the release snapshot pins the exact released artifact: the inbox item's
    ``loa_request_sha256`` equals sha256(released LOA-request text) and is
    STABLE against post-release intake drift (m6);
  - the urgency badge fact: an emergency case releases with
    ``emergency: true``; a non-emergency case with ``false`` (M15);
  - the check payload's four-bucket totals and the
    ``awaiting-external-party`` ledger state when the received LOA is not
    recorded (M2);
  - the package payload's ``human_acts_outstanding`` (readiness is never a
    bare boolean — ethics 9).

Socketless in-process requests through the REAL Handler — no port is ever
bound (the live server on 8765 is never touched).
"""

import contextlib
import copy
import hashlib
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

from ossicro.review_port import DeterministicStubReviewer   # noqa: E402

ACTOR = "Jordan A. Rivera, MD"
RELEASER = "Dana Q. Osei, MD"
LOA = "manufacturer-letter-of-authorization"


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


class P4TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p4-tests-")
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

    def _register(self, case_id, case):
        server.CASES[case_id] = case
        self._case_ids.append(case_id)
        return case

    def _committed_case(self, case_id, overrides=None, drop=()):
        case = server._new_case()
        fields = dict(server._sample_payload()["fields"])
        for key in drop:
            fields.pop(key, None)
        fields.update(overrides or {})
        _write_intake(case, fields)
        self._register(case_id, case)
        body, status = server._profile_commit(case, {"actor": ACTOR})
        assert status == 200, body
        return case

    def _released_case(self, case_id, overrides=None):
        case = self._committed_case(case_id, overrides)
        server._generate_payload(case)
        status, body = _http("POST", "/api/case/%s/release" % case_id,
                             {"actor": RELEASER, "to": "manufacturer"})
        assert status == 200, body
        return case

    def _inbox_item(self, case):
        rid = case["released"]["release_id"]
        status, body = _http("GET", "/api/manufacturer/inbox")
        assert status == 200
        return next(i for i in body["inbox"] if i["release_id"] == rid)


class TestReleaseArtifactHash(P4TestBase):

    def test_snapshot_hash_matches_released_text(self):
        case = self._released_case("p4hashok")
        item = self._inbox_item(case)
        self.assertEqual(
            item["loa_request_sha256"],
            hashlib.sha256(item["loa_request"].encode("utf-8")).hexdigest())
        self.assertEqual(item["loa_request_sha256"],
                         case["released"]["loa_request_sha256"])

    def test_snapshot_hash_stable_against_post_release_drift(self):
        case = self._released_case("p4hashstable")
        before = self._inbox_item(case)
        _write_intake(case, {"drug.name": "DriftedDrugX"})
        after = self._inbox_item(case)
        self.assertEqual(before["loa_request_sha256"],
                         after["loa_request_sha256"])
        # the snapshot text still re-hashes to the pinned value
        self.assertEqual(
            after["loa_request_sha256"],
            hashlib.sha256(after["loa_request"].encode("utf-8")).hexdigest())

    def test_release_never_mutates_intake(self):
        case = self._committed_case("p4nomut")
        server._generate_payload(case)
        before = copy.deepcopy(case["intake"])
        _http("POST", "/api/case/p4nomut/release",
              {"actor": RELEASER, "to": "manufacturer"})
        self.assertEqual(case["intake"], before)


class TestUrgencyBadge(P4TestBase):

    def test_non_emergency_release_is_not_badged(self):
        case = self._released_case("p4calm")
        self.assertIs(self._inbox_item(case)["emergency"], False)

    def test_emergency_release_is_badged_and_urgent_in_text(self):
        case = self._released_case("p4urgent", overrides={
            "submission.emergency": "true",
            "submission.emergency_auth_datetime": "2026-07-01",
            "submission.first_treatment_date": "2026-07-01",
        })
        item = self._inbox_item(case)
        self.assertIs(item["emergency"], True)
        self.assertIn("URGENCY: EMERGENCY REQUEST (21 CFR 312.310(d))",
                      item["loa_request"])


class TestAwaitingExternalPartyInCheck(P4TestBase):

    def test_check_totals_carry_the_fourth_bucket(self):
        case = self._committed_case("p4tot")
        payload = server._check_payload(case)
        self.assertIn("awaiting-external-party", payload["totals"])
        # sample records the received LOA -> nothing awaiting
        self.assertEqual(payload["totals"]["awaiting-external-party"], 0)

    def test_loa_awaits_external_party_until_receipt_recorded(self):
        case = self._committed_case(
            "p4await", drop=("manufacturer.loa_received_date",
                             "manufacturer.loa_signatory"))
        payload = server._check_payload(case)
        item = next(i for i in payload["ledger"] if i["doc_id"] == LOA)
        self.assertEqual(item["status"], "awaiting-external-party")
        self.assertEqual(payload["totals"]["awaiting-external-party"], 1)
        self.assertIn("OSSICRO's draft for their review",
                      item["questions"][0]["text"])

    def test_recording_the_receipt_turns_the_row_green(self):
        case = self._committed_case(
            "p4green", drop=("manufacturer.loa_received_date",
                             "manufacturer.loa_signatory"))
        _write_intake(case, {
            "manufacturer.loa_received_date": "2026-06-20",
            "manufacturer.loa_signatory": "Dana Q. Example, VP Regulatory",
        })
        body, status = server._profile_confirm(case, {
            "actor": ACTOR,
            "field_ids": ["manufacturer.loa_received_date",
                          "manufacturer.loa_signatory"]})
        assert status == 200, body
        payload = server._check_payload(case)
        item = next(i for i in payload["ledger"] if i["doc_id"] == LOA)
        self.assertEqual(item["status"], "green")
        self.assertTrue(any("received, signed instrument recorded" in n
                            for n in item["notes"]))


class TestHumanActsOutstandingInPackage(P4TestBase):

    def test_package_names_the_outstanding_human_acts(self):
        case = self._committed_case("p4acts")
        server._generate_payload(case)
        pkg = server._package_payload(case)
        self.assertTrue(pkg["submission_ready"])
        acts = pkg["human_acts_outstanding"]
        self.assertTrue(acts)                      # never a bare boolean
        self.assertTrue(all(a["kind"] == "gate" for a in acts))

    def test_unreceived_loa_blocks_and_appears_as_external_act(self):
        case = self._committed_case(
            "p4blocked", drop=("manufacturer.loa_received_date",
                               "manufacturer.loa_signatory"))
        server._generate_payload(case)
        pkg = server._package_payload(case)
        self.assertFalse(pkg["submission_ready"])
        self.assertTrue(any("Manufacturer LOA not yet received" in b["message"]
                            for b in pkg["blocking"]))
        ext = [a for a in pkg["human_acts_outstanding"]
               if a["kind"] == "external-party"]
        self.assertEqual([a["id"] for a in ext], [LOA])
        self.assertEqual(ext[0]["who"], "manufacturer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
