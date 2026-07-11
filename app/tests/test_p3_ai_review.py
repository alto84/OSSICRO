"""Overhaul P3 — AI-review attribution + reviewer disposition (B1 full
remediation, HC5) app-side tests.

Covers:
  - one ``ai_review`` audit record per LIVE concept review (monkeypatched
    fake live reviewer): actor ``system:concept-reviewer``, model id +
    version, doc ids, finding count, destination ``anthropic-api`` — flat and
    value-free (INV-8), persisted to disk, hash-chain intact;
  - NO ``ai_review`` record on the stub path (no egress happened);
  - the /package path writes the record too, carrying the COMMITTED hash;
  - the check-screen reviewer disclosure, composed from the claim registry
    (``ai-review-live`` / ``ai-review-offline``) — never silent either way;
  - stable content-derived ``finding_id`` on every concept finding;
  - POST /api/case/{id}/review-disposition round-trip: validation, the
    ``ai_review_disposition`` audit record (note text stays OUT of the
    trail), the check payload's review_dispositions map, and escalate-only
    (a disposition never changes ledger state);
  - the _select_reviewer env matrix: the live reviewer is selected ONLY when
    OSSICRO_LIVE_CONCEPT_REVIEW is affirmative AND a key is present; every
    other combination — and any construction failure — yields the offline
    stub. (The unset-flag-with-key case is ALSO asserted from the engine
    boundary suite, engine/tests/test_fhir_ingest.py PT-5.)

The suite never binds :8765 — all HTTP runs through the socketless in-process
harness.
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import server  # noqa: E402  (imports the engine; never binds the port)

from ossicro.review_claude import ClaudeConceptReviewer  # noqa: E402
from ossicro.review_port import (  # noqa: E402
    ConceptFinding,
    DeterministicStubReviewer,
    ReviewReport,
)

ACTOR = "Jordan A. Rivera, MD"
DRUG = "Zaltrexafil"   # synthetic, distinctive — lands in rendered draft text


class _FakeLiveReviewer:
    """A stand-in for the live Claude reviewer: NOT the deterministic stub,
    so the server treats it as egress. Quotes the intake-filled drug name so
    the finding survives validate_report (the span exists verbatim in the
    rendered document and is not template-locked)."""

    model = "claude-fake-live"
    model_id = "claude-fake-live"
    model_version = "claude-fake-live-20260711"

    def review(self, text, doc, principles):
        report = ReviewReport(model=self.model)
        if DRUG in (text or ""):
            report.findings.append(ConceptFinding(
                principle_id="P2", severity="advisory", span=DRUG,
                message="synthetic advisory finding (test only)",
                suggestion=""))
        return report


# ---------------------------------------------------------------------------
# Socketless in-process HTTP (same harness as test_p2_claims_schema).
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
    payload = b"" if body is None else json.dumps(body).encode("utf-8")
    raw = ("%s %s HTTP/1.1\r\nHost: test\r\nConnection: close\r\n"
           "Content-Length: %d\r\n\r\n" % (method, path, len(payload))
           ).encode("ascii") + payload
    sock = _FakeSocket(raw)
    with contextlib.redirect_stderr(io.StringIO()):
        server.Handler(sock, ("127.0.0.1", 0), None)
    head, _, resp_body = bytes(sock.out).partition(b"\r\n\r\n")
    status = int(head.split(None, 2)[1])
    return status, resp_body


def _http(method, path, body=None):
    status, resp = _http_raw(method, path, body)
    return status, json.loads(resp.decode("utf-8"))


class P3TestBase(unittest.TestCase):
    """Default reviewer = the offline stub; individual tests flip to the
    fake live reviewer explicitly."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p3-tests-")
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

    def _use_live(self):
        server._select_reviewer = lambda: _FakeLiveReviewer()

    def _new_case_id(self):
        status, body = _http("POST", "/api/case", {})
        self.assertEqual(status, 200)
        case_id = body["case_id"]
        self._case_ids.append(case_id)
        return case_id

    def _case_with_drug(self):
        case_id = self._new_case_id()
        status, body = _http("POST", "/api/case/%s/intake" % case_id,
                             {"fields": {"drug.name": DRUG}, "actor": ACTOR})
        self.assertEqual(status, 200, body)
        return case_id

    def _audit(self, case_id):
        status, body = _http("GET", "/api/case/%s/audit" % case_id)
        self.assertEqual(status, 200)
        return body

    def _records(self, case_id, action):
        return [r for r in self._audit(case_id)["audit"]
                if r.get("action") == action]


# ---------------------------------------------------------------------------
# HC5: one ai_review audit record per LIVE review; none on the stub path
# ---------------------------------------------------------------------------

class TestAiReviewAuditRecord(P3TestBase):
    def test_live_check_writes_one_ai_review_record(self):
        self._use_live()
        case_id = self._case_with_drug()
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        recs = self._records(case_id, "ai_review")
        self.assertEqual(len(recs), 1)
        rec = recs[0]
        self.assertEqual(rec["actor"], "system:concept-reviewer")
        self.assertEqual(rec["target"], "concept-review")
        self.assertEqual(rec["input_hash"], "")   # uncommitted: honest absence
        d = rec["detail"]
        self.assertEqual(d["model"], "claude-fake-live")
        self.assertEqual(d["model_version"], "claude-fake-live-20260711")
        self.assertEqual(d["destination"], "anthropic-api")
        self.assertGreaterEqual(d["finding_count"], 1)
        self.assertTrue(d["doc_ids"])            # the reviewed documents
        # INV-8: value-free — no document text, no finding span in the record.
        self.assertNotIn(DRUG, json.dumps(rec))
        # Tamper-evidence chain still verifies with the new record type.
        self.assertTrue(self._audit(case_id)["chain_ok"])

    def test_live_record_is_persisted_to_disk(self):
        self._use_live()
        case_id = self._case_with_drug()
        status, _ = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        with open(os.path.join(server.CASES_DIR, case_id + ".json"),
                  encoding="utf-8") as f:
            on_disk = json.load(f)
        self.assertTrue(any(r.get("action") == "ai_review"
                            for r in on_disk["audit"]))

    def test_stub_check_writes_no_ai_review_record(self):
        case_id = self._case_with_drug()
        status, _ = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(self._records(case_id, "ai_review"), [])

    def test_live_package_writes_record_with_committed_hash(self):
        self._use_live()
        case_id = self._case_with_drug()
        status, body = _http("POST", "/api/case/%s/profile/commit" % case_id,
                             {"actor": ACTOR})
        self.assertEqual(status, 200, body)
        committed_hash = body["profile"]["profile_hash"]
        status, _ = _http("GET", "/api/case/%s/package" % case_id)
        self.assertEqual(status, 200)
        recs = self._records(case_id, "ai_review")
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["input_hash"], committed_hash)

    def test_stub_package_writes_no_record(self):
        case_id = self._case_with_drug()
        status, _ = _http("POST", "/api/case/%s/profile/commit" % case_id,
                          {"actor": ACTOR})
        self.assertEqual(status, 200)
        status, _ = _http("GET", "/api/case/%s/package" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(self._records(case_id, "ai_review"), [])


# ---------------------------------------------------------------------------
# UI disclosure — from the claim registry, never silent either way
# ---------------------------------------------------------------------------

class TestReviewerDisclosure(P3TestBase):
    def test_disclosure_claims_are_registered(self):
        for cid in ("ai-review-live", "ai-review-offline"):
            self.assertIn(cid, server.CLAIM_REGISTRY)

    def test_stub_disclosure(self):
        case_id = self._case_with_drug()
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        rv = check["reviewer"]
        self.assertFalse(rv["live"])
        self.assertEqual(rv["disclosure"],
                         server._claim_text("ai-review-offline"))

    def test_live_disclosure_names_the_model(self):
        self._use_live()
        case_id = self._case_with_drug()
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        rv = check["reviewer"]
        self.assertTrue(rv["live"])
        expected = server._claim_text("ai-review-live").replace(
            "{model}", "claude-fake-live")
        self.assertEqual(rv["disclosure"], expected)
        self.assertIn("claude-fake-live", rv["disclosure"])


# ---------------------------------------------------------------------------
# finding_id: stable, content-derived, rides every concept finding
# ---------------------------------------------------------------------------

class TestFindingIds(P3TestBase):
    def test_findings_carry_stable_ids(self):
        self._use_live()
        case_id = self._case_with_drug()
        status, first = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        findings = [f for fl in first["concept_by_doc"].values() for f in fl]
        self.assertTrue(findings)
        for f in findings:
            self.assertTrue(f["finding_id"].startswith("cf-"), f)
        status, second = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(
            {f["finding_id"] for fl in first["concept_by_doc"].values() for f in fl},
            {f["finding_id"] for fl in second["concept_by_doc"].values() for f in fl})


# ---------------------------------------------------------------------------
# POST /review-disposition — HC5 disposition capture, escalate-only
# ---------------------------------------------------------------------------

class TestReviewDispositionEndpoint(P3TestBase):
    def _one_finding_id(self, case_id):
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        findings = [f for fl in check["concept_by_doc"].values() for f in fl]
        self.assertTrue(findings)
        return findings[0]["finding_id"], check

    def test_validation_matrix(self):
        case_id = self._case_with_drug()
        url = "/api/case/%s/review-disposition" % case_id
        status, body = _http("POST", url,
                             {"finding_id": "cf-x", "disposition": "accepted"})
        self.assertEqual(status, 400)          # no actor
        self.assertIn("actor", body["error"])
        status, body = _http("POST", url,
                             {"actor": ACTOR, "disposition": "accepted"})
        self.assertEqual(status, 400)          # no finding_id
        self.assertIn("finding_id", body["error"])
        status, body = _http("POST", url,
                             {"actor": ACTOR, "finding_id": "cf-x",
                              "disposition": "approved-and-cleared"})
        self.assertEqual(status, 400)          # invalid disposition verb
        self.assertEqual(body["allowed"], ["accepted", "dismissed"])
        status, _ = _http("POST", "/api/case/nope-nope/review-disposition",
                          {"actor": ACTOR, "finding_id": "cf-x",
                           "disposition": "accepted"})
        self.assertEqual(status, 404)          # unknown case

    def test_round_trip_and_audit_record(self):
        self._use_live()
        case_id = self._case_with_drug()
        fid, _ = self._one_finding_id(case_id)
        status, body = _http("POST",
                             "/api/case/%s/review-disposition" % case_id,
                             {"actor": ACTOR, "finding_id": fid,
                              "disposition": "dismissed"})
        self.assertEqual(status, 200, body)
        self.assertTrue(body["ok"])
        self.assertEqual(body["disposition"]["disposition"], "dismissed")
        self.assertEqual(body["disposition"]["actor"], ACTOR)
        recs = self._records(case_id, "ai_review_disposition")
        self.assertEqual(len(recs), 1)
        rec = recs[0]
        self.assertEqual(rec["actor"], ACTOR)
        self.assertEqual(rec["target"], fid)
        self.assertEqual(rec["detail"]["disposition"], "dismissed")
        self.assertEqual(rec["detail"]["finding_id"], fid)
        self.assertFalse(rec["detail"]["note_recorded"])
        self.assertTrue(self._audit(case_id)["chain_ok"])
        # the check payload now maps the finding to its latest disposition
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(check["review_dispositions"][fid]["disposition"],
                         "dismissed")

    def test_note_text_stays_out_of_the_audit_trail(self):
        self._use_live()
        case_id = self._case_with_drug()
        fid, _ = self._one_finding_id(case_id)
        note = "Reviewed against the source chart myself; the phrasing is fine."
        status, body = _http("POST",
                             "/api/case/%s/review-disposition" % case_id,
                             {"actor": ACTOR, "finding_id": fid,
                              "disposition": "accepted", "note": note})
        self.assertEqual(status, 200, body)
        rec = self._records(case_id, "ai_review_disposition")[0]
        self.assertTrue(rec["detail"]["note_recorded"])
        self.assertNotIn(note, json.dumps(self._audit(case_id)["audit"]))
        # ... but the note IS kept with the disposition record on the case
        # (like a sign-off statement — retrievable, not chained-immutable).
        status, check = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(check["review_dispositions"][fid]["note"], note)

    def test_disposition_is_escalate_only(self):
        # Recording a disposition must not move a single ledger status —
        # dispositions record judgment; they never clear or demote anything.
        self._use_live()
        case_id = self._case_with_drug()
        fid, before = self._one_finding_id(case_id)
        status, _ = _http("POST",
                          "/api/case/%s/review-disposition" % case_id,
                          {"actor": ACTOR, "finding_id": fid,
                           "disposition": "accepted"})
        self.assertEqual(status, 200)
        status, after = _http("GET", "/api/case/%s/check" % case_id)
        self.assertEqual(status, 200)
        self.assertEqual(
            [(i["doc_id"], i["status"]) for i in before["ledger"]],
            [(i["doc_id"], i["status"]) for i in after["ledger"]])
        self.assertEqual(before["totals"], after["totals"])


# ---------------------------------------------------------------------------
# _select_reviewer env matrix (B1: the opt-in is the ONLY path to egress)
# ---------------------------------------------------------------------------

class TestSelectReviewerMatrix(unittest.TestCase):
    """Runs against the REAL server._select_reviewer (no monkeypatched
    selector here) with a controlled environment."""

    def _env(self, flag, key):
        # patch.dict snapshots os.environ and restores it at cleanup, so
        # in-test pops/sets below are safe.
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("OSSICRO_LIVE_CONCEPT_REVIEW", None)
        os.environ.pop("ANTHROPIC_API_KEY", None)
        if flag is not None:
            os.environ["OSSICRO_LIVE_CONCEPT_REVIEW"] = flag
        if key is not None:
            os.environ["ANTHROPIC_API_KEY"] = key

    def test_stub_when_flag_unset_even_with_key(self):
        self._env(flag=None, key="sk-synthetic-test")
        self.assertIsInstance(server._select_reviewer(),
                              DeterministicStubReviewer)

    def test_stub_on_non_affirmative_flag(self):
        for value in ("", "0", "false", "no", "off"):
            self._env(flag=value, key="sk-synthetic-test")
            self.assertIsInstance(server._select_reviewer(),
                                  DeterministicStubReviewer, value)

    def test_stub_when_flag_set_but_no_key(self):
        self._env(flag="1", key=None)
        self.assertIsInstance(server._select_reviewer(),
                              DeterministicStubReviewer)

    def test_live_selected_only_with_flag_and_key(self):
        self._env(flag="1", key="sk-synthetic-test")
        sentinel = _FakeLiveReviewer()
        with mock.patch.object(ClaudeConceptReviewer, "from_anthropic",
                               classmethod(lambda cls, *a, **k: sentinel)):
            self.assertIs(server._select_reviewer(), sentinel)

    def test_construction_failure_falls_back_to_stub(self):
        self._env(flag="1", key="sk-synthetic-test")

        def _boom(cls, *a, **k):
            raise RuntimeError("no SDK in this environment")

        with mock.patch.object(ClaudeConceptReviewer, "from_anthropic",
                               classmethod(_boom)):
            self.assertIsInstance(server._select_reviewer(),
                                  DeterministicStubReviewer)


# ---------------------------------------------------------------------------
# ClaudeConceptReviewer attribution surface (no network — constructor only)
# ---------------------------------------------------------------------------

class TestReviewerAttributionSurface(unittest.TestCase):
    def test_model_id_and_version_exposed(self):
        r = ClaudeConceptReviewer(client=None, model="claude-sonnet-5")
        self.assertEqual(r.model_id, "claude-sonnet-5")
        self.assertEqual(r.model_version, "claude-sonnet-5")  # pin = version
        r2 = ClaudeConceptReviewer(client=None, model="claude-sonnet-5",
                                   model_version="claude-sonnet-5-20260601")
        self.assertEqual(r2.model_version, "claude-sonnet-5-20260601")


if __name__ == "__main__":
    unittest.main(verbosity=2)
