"""Overhaul P2 — app-side tests: schema round-trip and the claim registry.

Covers:
  - every P2 intake field is accepted by POST /intake (schema round-trip via
    the REAL Handler, socketless — the suite never binds :8765) and is
    reachable by the fix-loop (a ledger question naming the field id maps
    back to it);
  - [PT-3]: the claim registry rides the /schema payload and is injected
    into the served index.html boot payload; the server's patient notice is
    COMPOSED from the registry;
  - the claim-duplication tripwire: a registered claim's distinctive text
    must not appear hardcoded in the app's product surfaces (server.py,
    static/*.html) — the only authored copy lives in
    engine/registry/claims.json. (This is the tripwire that would have
    caught the third hardcoded "Still in draft.")
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

# The P2 field contract (mirrors engine/tests/test_p2_registry.py) with a
# synthetic, clearly-fictional value for each.
P2_FIELD_VALUES = {
    "submission.date": "2026-06-15",
    "manufacturer.loa_received_date": "2026-06-20",
    "manufacturer.loa_signatory": "Dana Q. Example, VP Regulatory, Helix Therapeutics",
    "manufacturer.loa_document_sha256": "0" * 64,
    "submission.fda_authorization_date": "2026-07-01",
    "treatment.conclusion_date": "2026-12-15",
    "consent.timing_attestation": "obtained-before-treatment",
    "consent.injury_compensation_statement": (
        "If you are injured as a result of this treatment, medical care is "
        "available at the treating facility; costs may be billed to you or "
        "your insurer. Contact Dr. Rivera for more information."),
    "consent.cost_statement": (
        "You will not be charged for the investigational drug itself; "
        "standard-of-care costs may be billed to you or your insurer."),
    "drug.quantity_requested": "Two 28-day cycles (112 tablets)",
    "submission.needed_by_date": "2026-07-20",
    "submission.cost_recovery_statement": (
        "No charge to the patient for the drug; no cost recovery under "
        "21 CFR 312.8 is requested."),
}


# ---------------------------------------------------------------------------
# Socketless in-process HTTP (same harness as test_wave1_hardening).
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
    """One in-process request through server.Handler -> (status, bytes body)."""
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


class P2TestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p2-tests-")
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

    def _new_case_id(self):
        status, body = _http("POST", "/api/case", {})
        self.assertEqual(status, 200)
        case_id = body["case_id"]
        self._case_ids.append(case_id)
        return case_id


# ---------------------------------------------------------------------------
# Schema round-trip: every P2 field accepted by /intake, fix-loop reachable
# ---------------------------------------------------------------------------

class TestP2SchemaRoundTrip(P2TestBase):
    def test_every_new_field_in_schema_payload(self):
        ids = {f["id"] for f in server._schema_payload()["fields"]}
        for field_id in P2_FIELD_VALUES:
            self.assertIn(field_id, ids)

    def test_intake_accepts_and_returns_every_new_field(self):
        case_id = self._new_case_id()
        status, body = _http("POST", "/api/case/%s/intake" % case_id,
                             {"fields": dict(P2_FIELD_VALUES), "actor": ACTOR})
        self.assertEqual(status, 200, body)
        self.assertTrue(body.get("ok"))
        status, body = _http("GET", "/api/case/%s" % case_id)
        self.assertEqual(status, 200)
        for field_id, value in P2_FIELD_VALUES.items():
            self.assertEqual(body["intake"].get(field_id), value, field_id)

    def test_every_new_field_reachable_by_fix_loop(self):
        # A ledger question that names the field id must map back to the
        # intake field (the SPA's fix-loop jump).
        for field_id in P2_FIELD_VALUES:
            q = "Provide '%s' for the document (required by its authority)." % field_id
            self.assertEqual(server._field_id_for_question(q), field_id)

    def test_sample_fixture_posts_clean_through_intake(self):
        # M7 side effect: with the dispensing-time pseudo-fields gone, the
        # whole synthetic sample is schema-valid intake.
        case_id = self._new_case_id()
        fields = server._sample_payload()["fields"]
        status, body = _http("POST", "/api/case/%s/intake" % case_id,
                             {"fields": fields, "actor": ACTOR})
        self.assertEqual(status, 200, body)


# ---------------------------------------------------------------------------
# [PT-3] claims: one authored copy, injected boot payload, composed strings
# ---------------------------------------------------------------------------

CLAIM_IDS = ("nothing-submitted-to-fda", "chart-data-stays-local",
             "drafts-only-banner", "no-direct-identifiers-in-view")


class TestClaimsInjection(P2TestBase):
    def test_schema_payload_carries_the_claims(self):
        claims = server._schema_payload()["claims"]
        for cid in CLAIM_IDS:
            self.assertIn(cid, claims)
            self.assertTrue(claims[cid]["text"].strip())
            self.assertTrue(claims[cid]["true_when"].strip())

    def test_index_html_served_with_injected_registry(self):
        status, html = _http_raw("GET", "/")
        self.assertEqual(status, 200)
        self.assertNotIn(b"window.OSSICRO_CLAIMS = null", html)
        self.assertIn(b"window.OSSICRO_CLAIMS = {", html)
        for cid in CLAIM_IDS:
            self.assertIn(cid.encode("ascii"), html)

    def test_index_html_source_still_carries_the_marker(self):
        # The file on disk must keep the marker the server replaces.
        path = os.path.join(server.STATIC_DIR, "index.html")
        with open(path, encoding="utf-8") as f:
            src = f.read()
        self.assertIn("window.OSSICRO_CLAIMS = null", src)

    def test_patient_notice_composed_from_the_registry(self):
        claim = server._claim_text("nothing-submitted-to-fda")
        self.assertIn(claim, server.STRINGS["patient_notice"])
        # draft-stage patient view renders it; the enrolled notice does not
        # (the claim would be false there — MAJOR-2).
        case = server._new_case()
        self.assertIn(claim, server._patient_view(case)["notice"])
        case["enrollment"] = {"actor": ACTOR, "at": "2026-07-11T00:00:00Z",
                              "legal_basis": "treatment-disclosure"}
        self.assertNotIn(claim, server._patient_view(case)["notice"])

    def test_claim_text_fails_loud_on_unregistered_id(self):
        with self.assertRaises(KeyError):
            server._claim_text("no-such-claim")


class TestClaimDuplicationTripwire(unittest.TestCase):
    """A registered claim's distinctive text must not appear hardcoded in the
    app's product surfaces — the registry/render path is the only copy.
    Tests are excluded: an assertion pinning rendered output is verification,
    not a second authored copy."""

    def _product_sources(self):
        sources = []
        server_py = os.path.join(APP_DIR, "server.py")
        with open(server_py, encoding="utf-8") as f:
            sources.append(("app/server.py", f.read()))
        static_dir = os.path.join(APP_DIR, "static")
        for name in sorted(os.listdir(static_dir)):
            if name.endswith((".html", ".js")):
                with open(os.path.join(static_dir, name), encoding="utf-8") as f:
                    sources.append(("app/static/" + name, f.read()))
        return sources

    def test_no_registered_claim_text_hardcoded_in_app(self):
        offenders = []
        for cid, claim in server.CLAIM_REGISTRY.items():
            needle = claim["tripwire"].lower()
            for path, text in self._product_sources():
                if needle in text.lower():
                    offenders.append("%s: claim %r (tripwire %r)"
                                     % (path, cid, claim["tripwire"]))
        self.assertEqual(offenders, [],
                         "registered claim text appears outside the "
                         "registry/render path:\n" + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main(verbosity=2)
