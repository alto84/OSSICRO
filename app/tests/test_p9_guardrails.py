"""Overhaul P9 app tests: deployment guardrails and store hardening.

Covers (spec: docs/overhaul/OVERHAUL-PLAN.md, Package 9):
  - M9a bind-guard refusal matrix: loopback always allowed; a non-loopback
    HOST refused without the override; refused WITH the override while no
    auth backend exists (today: always — _auth_backend_configured() is
    hard-coded False); main() exits non-zero and never constructs the
    server object. NO PORT IS EVER BOUND by these tests (the live UI-QA
    server on 8765 is never touched).
  - m17 token hygiene: the patient token is masked out of log_message
    output, and token lookup (hmac.compare_digest index) still resolves
    the right case / 404s an unknown token.
  - m15 POST durability: an injected _save_case failure surfaces as an
    honest 500 memory-disk-divergence message, never a raw traceback.
  - m18 export act: POST /api/case/{id}/export {actor, format} writes
    exactly one 'export' audit record and returns the DRAFT bytes; the
    INV-3 gate and the named-actor requirement fail closed.
  - m20 identifier lint at release time: fires on seeded identifier text
    (naming the field, never the text), stays silent on the sample case,
    and NEVER blocks the release.
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
# Socketless in-process HTTP (same rig as test_wave1_hardening): drive the
# REAL Handler without ever binding a port.
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
    """One in-process request -> (status, header_text, raw_body_bytes)."""
    payload = b"" if body is None else json.dumps(body).encode("utf-8")
    raw = ("%s %s HTTP/1.1\r\nHost: test\r\nConnection: close\r\n"
           "Content-Length: %d\r\n\r\n" % (method, path, len(payload))
           ).encode("ascii") + payload
    sock = _FakeSocket(raw)
    with contextlib.redirect_stderr(io.StringIO()):   # quiet request logging
        server.Handler(sock, ("127.0.0.1", 0), None)
    head, _, resp_body = bytes(sock.out).partition(b"\r\n\r\n")
    status = int(head.split(None, 2)[1])
    return status, head.decode("latin-1"), resp_body


def _http(method, path, body=None):
    status, _head, resp_body = _http_raw(method, path, body)
    return status, json.loads(resp_body.decode("utf-8"))


class P9TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p9-tests-")
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

    def _committed_sample(self, case_id):
        case = self._register(case_id, self._sample_case())
        status, body = _http("POST", "/api/case/%s/profile/commit" % case_id,
                             {"actor": ACTOR})
        assert status == 200, body
        return case


# ---------------------------------------------------------------------------
# M9a — the bind-guard refusal matrix
# ---------------------------------------------------------------------------

@contextlib.contextmanager
def _env(name, value):
    prior = os.environ.get(name)
    try:
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value
        yield
    finally:
        if prior is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = prior


class TestBindGuard(unittest.TestCase):

    def test_loopback_always_allowed(self):
        for host in ("127.0.0.1", "127.5.6.7", "localhost", "::1",
                     "LOCALHOST"):
            self.assertIsNone(server._bind_refusal(host), host)

    def test_non_loopback_refused_without_override(self):
        with _env("OSSICRO_ALLOW_NONLOCAL_BIND", None):
            for host in ("0.0.0.0", "192.168.1.50", "::", "example.internal"):
                reason = server._bind_refusal(host)
                self.assertIsNotNone(reason, host)
                self.assertIn("INV-7", reason)
                self.assertIn("REFUSING", reason)

    def test_non_affirmative_override_value_still_refused(self):
        for value in ("0", "true", "yes", " "):   # only "1" is the override
            with _env("OSSICRO_ALLOW_NONLOCAL_BIND", value):
                self.assertIsNotNone(server._bind_refusal("0.0.0.0"), value)

    def test_override_without_auth_backend_cannot_succeed(self):
        # The override env var alone must NOT open the wall: no auth backend
        # exists in this build, so the second leg fails — and says so.
        with _env("OSSICRO_ALLOW_NONLOCAL_BIND", "1"):
            reason = server._bind_refusal("0.0.0.0")
            self.assertIsNotNone(reason)
            self.assertIn("INV-7", reason)
            self.assertIn("authentication backend", reason)

    def test_auth_backend_is_hardcoded_absent(self):
        # The guard's second leg is structurally False today. If this test
        # ever fails, an auth backend was added — re-review the bind guard
        # and DEPLOYMENT-COMPLIANCE.md as part of that change.
        self.assertFalse(server._auth_backend_configured())

    def test_both_legs_true_would_allow(self):
        # The override is real, not theater: with BOTH legs satisfied the
        # guard opens. (Patched here; in the shipped build the second leg
        # cannot be satisfied.)
        orig = server._auth_backend_configured
        server._auth_backend_configured = lambda: True
        try:
            with _env("OSSICRO_ALLOW_NONLOCAL_BIND", "1"):
                self.assertIsNone(server._bind_refusal("0.0.0.0"))
        finally:
            server._auth_backend_configured = orig

    def test_main_refuses_nonlocal_host_and_never_binds(self):
        # main() with a patched non-loopback HOST exits non-zero BEFORE the
        # server object is ever constructed — the suite never binds a port.
        orig_host = server.HOST
        orig_httpd = server.ThreadingHTTPServer

        def _bomb(*a, **k):   # pragma: no cover — reaching this is the failure
            raise AssertionError("ThreadingHTTPServer must never be "
                                 "constructed on a refused bind")

        server.HOST = "0.0.0.0"
        server.ThreadingHTTPServer = _bomb
        try:
            with _env("OSSICRO_ALLOW_NONLOCAL_BIND", None):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as ctx:
                        server.main()
                self.assertNotEqual(ctx.exception.code, 0)
                self.assertIn("INV-7", stderr.getvalue())
        finally:
            server.HOST = orig_host
            server.ThreadingHTTPServer = orig_httpd


# ---------------------------------------------------------------------------
# m17 — token hygiene
# ---------------------------------------------------------------------------

class TestTokenHygiene(P9TestBase):

    def test_log_message_masks_patient_token(self):
        h = server.Handler.__new__(server.Handler)   # no socket, no bind
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            h.log_message('"GET /api/patient/%s HTTP/1.1" 200 -',
                          "f00dfeedfacecafef00dfeedfacecafe")
        logged = buf.getvalue()
        self.assertNotIn("f00dfeedfacecafe", logged)
        self.assertIn("/api/patient/<token-masked>", logged)
        # non-patient paths are untouched
        buf2 = io.StringIO()
        with contextlib.redirect_stderr(buf2):
            h.log_message('"GET /api/case/abc123 HTTP/1.1" 200 -')
        self.assertIn("/api/case/abc123", buf2.getvalue())

    def test_token_lookup_resolves_and_unknown_404s(self):
        case = self._committed_sample("p9token1")
        status, body = _http("POST", "/api/case/p9token1/patient-link",
                             {"actor": ACTOR})
        self.assertEqual(status, 200)
        token = body["patient_token"]
        # index-based compare_digest lookup finds the case...
        self.assertIs(server._case_for_patient_token(token), case)
        self.assertIn(token, server._patient_token_index())
        # ...through the real endpoint too
        status, view = _http("GET", "/api/patient/%s" % token)
        self.assertEqual(status, 200)
        self.assertNotIn("case_id", view)
        # unknown token: plain 404, token never echoed back
        status, err = _http("GET", "/api/patient/%s" % ("e" * 32))
        self.assertEqual(status, 404)
        self.assertNotIn("e" * 32, json.dumps(err))
        self.assertIsNone(server._case_for_patient_token("e" * 32))
        self.assertIsNone(server._case_for_patient_token(None))


# ---------------------------------------------------------------------------
# m15 — POST durability: the honest memory-disk-divergence 500
# ---------------------------------------------------------------------------

class TestSaveFailureWrapper(P9TestBase):

    def _with_broken_save(self, fn):
        orig = server._save_case

        def _fail(case_id):
            raise OSError(28, "No space left on device")

        server._save_case = _fail
        try:
            return fn()
        finally:
            server._save_case = orig

    def test_commit_save_failure_returns_honest_500(self):
        case = self._register("p9save1", self._sample_case())
        status, body = self._with_broken_save(
            lambda: _http("POST", "/api/case/p9save1/profile/commit",
                          {"actor": ACTOR}))
        self.assertEqual(status, 500)
        self.assertTrue(body.get("diverged"))
        self.assertIn("DIVERGED", body["error"])
        self.assertIn("p9save1", body["error"])
        # honest divergence: the in-memory commit DID apply (nothing was
        # rolled back or hidden — the message says exactly that)
        self.assertIsNotNone(case.get("committed_profile"))

    def test_intake_and_signoff_save_failures_wrapped_too(self):
        self._register("p9save2", self._sample_case())
        status, body = self._with_broken_save(
            lambda: _http("POST", "/api/case/p9save2/intake",
                          {"fields": {"drug.dose": "10 mg"}}))
        self.assertEqual(status, 500)
        self.assertTrue(body.get("diverged"))
        status, body = self._with_broken_save(
            lambda: _http("POST", "/api/case",))
        self.assertEqual(status, 500)
        self.assertTrue(body.get("diverged"))

    def test_no_failure_no_wrapper(self):
        self._register("p9save3", self._sample_case())
        status, body = _http("POST", "/api/case/p9save3/profile/commit",
                             {"actor": ACTOR})
        self.assertEqual(status, 200)


# ---------------------------------------------------------------------------
# m18 — the export act
# ---------------------------------------------------------------------------

class TestExportAct(P9TestBase):

    def _export_records(self, case):
        return [r for r in case.get("audit", []) if r["action"] == "export"]

    def test_pdf_export_returns_bytes_and_one_audit_record(self):
        case = self._committed_sample("p9export1")
        status, head, body = _http_raw(
            "POST", "/api/case/p9export1/export",
            {"actor": ACTOR, "format": "pdf"})
        self.assertEqual(status, 200)
        self.assertIn("application/pdf", head)
        self.assertTrue(body.startswith(b"%PDF"))
        records = self._export_records(case)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["actor"], ACTOR)
        self.assertEqual(rec["detail"]["format"], "pdf")
        self.assertEqual(rec["target"],
                         "form-fda-3926-individual-patient-expanded-access")
        self.assertEqual(rec["input_hash"],
                         case["committed_profile"]["profile_hash"])
        # a second export is a second recorded act
        _http_raw("POST", "/api/case/p9export1/export",
                  {"actor": ACTOR, "format": "fdf"})
        self.assertEqual(len(self._export_records(case)), 2)

    def test_fdf_export_returns_fdf(self):
        self._committed_sample("p9export2")
        status, head, body = _http_raw(
            "POST", "/api/case/p9export2/export",
            {"actor": ACTOR, "format": "fdf"})
        self.assertEqual(status, 200)
        self.assertIn("application/vnd.fdf", head)
        self.assertTrue(body.startswith(b"%FDF"))

    def test_missing_actor_400_and_no_record(self):
        case = self._committed_sample("p9export3")
        status, body = _http("POST", "/api/case/p9export3/export",
                             {"format": "pdf"})
        self.assertEqual(status, 400)
        self.assertIn("actor", body["error"])
        self.assertEqual(self._export_records(case), [])

    def test_bad_format_400(self):
        self._committed_sample("p9export4")
        status, body = _http("POST", "/api/case/p9export4/export",
                             {"actor": ACTOR, "format": "docx"})
        self.assertEqual(status, 400)
        self.assertEqual(body["allowed"], ["fdf", "pdf"])

    def test_uncommitted_409_and_no_record(self):
        case = self._register("p9export5", self._sample_case())
        status, body = _http("POST", "/api/case/p9export5/export",
                             {"actor": ACTOR, "format": "pdf"})
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "UNCOMMITTED")
        self.assertEqual(self._export_records(case), [])

    def test_unknown_case_404(self):
        status, body = _http("POST", "/api/case/nope-nope-nope/export",
                             {"actor": ACTOR, "format": "pdf"})
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# m20 — the identifier lint at release time (escalate-only, never a block)
# ---------------------------------------------------------------------------

class TestReleaseIdentifierLint(P9TestBase):

    def _release(self, case_id):
        status, body = _http("POST", "/api/case/%s/generate" % case_id)
        assert status == 200, body
        return _http("POST", "/api/case/%s/release" % case_id,
                     {"actor": ACTOR, "to": "manufacturer"})

    def test_seeded_identifier_warns_but_never_blocks(self):
        case = self._register("p9lint1", self._sample_case())
        _write_intake(case, {
            "patient.no_alternative_basis":
                "No alternative; note patient name: Jane Doe, SSN "
                "123-45-6789, progressed 2025-11-03."})
        _http("POST", "/api/case/p9lint1/profile/commit", {"actor": ACTOR})
        status, body = self._release("p9lint1")
        self.assertEqual(status, 200)             # escalate-only: NOT a block
        lint = body["identifier_lint"]
        self.assertTrue(lint)
        fields = {w["field_id"] for w in lint}
        self.assertEqual(fields, {"patient.no_alternative_basis"})
        kinds = {w["kind"] for w in lint}
        self.assertLessEqual({"ssn", "date-like", "name-label"}, kinds)
        # the warning names the field, never the identifier itself
        blob = json.dumps(lint)
        self.assertNotIn("123-45-6789", blob)
        self.assertNotIn("Jane Doe", blob)
        # the warnings persist on the release record for later review
        self.assertEqual(case["released"]["identifier_lint"], lint)
        self.assertIn("never blocks", body["identifier_lint_note"])

    def test_sample_case_release_is_silent(self):
        self._committed_sample("p9lint2")
        status, body = self._release("p9lint2")
        self.assertEqual(status, 200)
        self.assertEqual(body["identifier_lint"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
