"""Overhaul P5 — ethics-gate honesty, app half.

Covers:
  - M4: the promote gate sweep. NON-EMERGENCY route: 409 while the
    informed-consent / irb-approval sign-offs are missing, unless the actor
    types acknowledge_unsigned_gates in their own words (min-length +
    not-a-placeholder enforced); the override, the advisories, and the
    external-fact gaps persist in case['enrollment'] and in the promote
    audit detail. EMERGENCY route: the same gaps are advisory only.
    Refusals mutate nothing.
  - M4 (render): the persisted advisories surface as ESCALATE-ONLY ledger
    notes in /check (status never changes) and in the payload's
    enrollment_advisories.
  - M13: for the informed-consent / irb-approval gates the sign-off
    statement must be the signer's own words (the server refuses absence,
    shortness, and the synthesized-placeholder shape) and the evidence
    object is persisted with the asked keys (blank = honest absence). The
    other gates keep the synthesized statement path.
  - m13b: a re-recorded sign-off SUPERSEDES the prior record (which stays,
    marked superseded_at/superseded_by); validity checks and /check read
    only non-superseded records.

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

from ossicro.review_port import DeterministicStubReviewer   # noqa: E402

ACTOR = "Jordan A. Rivera, MD"
ENROLLER = "Priya N. Kapoor, MD"

ACK = ("I am recording this enrollment before the consent and IRB "
       "sign-offs are recorded; both acts remain mine to perform.")

CONSENT_STATEMENT = ("I obtained the patient's written informed consent "
                     "myself on the date recorded here.")
IRB_STATEMENT = ("The IRB chair concurred with this individual-patient "
                 "treatment use after reviewing the request.")

# P6: both 3926 routes now carry the EA-profiled consent form; the ledger
# rows and gated sign-offs these tests exercise live on the EA doc id.
ICF_DOC = "informed-consent-form-part50-ea"
IRB_DOC = "irb-concurrence-request"


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
    status = int(head.decode("iso-8859-1").split("\r\n")[0].split(None, 2)[1])
    return status, json.loads(resp_body.decode("utf-8"))


class P5TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p5-tests-")
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

    def _committed_case(self, case_id, extra=None):
        case = server._new_case()
        fields = dict(server._sample_payload()["fields"])
        if extra:
            for key, value in extra.items():
                if value is None:
                    fields.pop(key, None)
                else:
                    fields[key] = value
        _write_intake(case, fields)
        self._register(case_id, case)
        body, status = server._profile_commit(case, {"actor": ACTOR})
        assert status == 200, body
        return case

    def _signoff(self, case_id, gate_id, doc_id, role, statement=None,
                 evidence=None, signer=ACTOR, date="2026-07-08"):
        body = {"gate_id": gate_id, "doc_id": doc_id, "signer_name": signer,
                "role": role, "date": date}
        if statement is not None:
            body["statement"] = statement
        if evidence is not None:
            body["evidence"] = evidence
        return _http("POST", "/api/case/%s/signoff" % case_id, body)

    def _sign_both_ethics_gates(self, case_id):
        status, _ = self._signoff(case_id, "informed-consent", ICF_DOC,
                                  "investigator", CONSENT_STATEMENT,
                                  {"consent_date": "2026-07-07"})
        assert status == 200
        status, _ = self._signoff(case_id, "irb-approval", IRB_DOC, "irb",
                                  IRB_STATEMENT,
                                  {"concurrence_date": "2026-07-08",
                                   "concurring_member": "Dr. P. Mfume (chair)",
                                   "irb_reference": "MRB-2026-114"},
                                  signer="Alex B. Chen, MD")
        assert status == 200


# ---------------------------------------------------------------------------
# M4 — the promote gate sweep: refusal / override / advisory matrix
# ---------------------------------------------------------------------------

class TestPromoteGateSweep(P5TestBase):

    def test_non_emergency_unsigned_gates_refused_without_ack(self):
        case = self._committed_case("p5refuse")
        before = copy.deepcopy(case)
        status, body = _http("POST", "/api/case/p5refuse/promote",
                             {"actor": ENROLLER,
                              "legal_basis": "authorization-164.508"})
        self.assertEqual(status, 409)
        self.assertTrue(body["acknowledgement_required"])
        self.assertIn("acknowledge_unsigned_gates", body["error"])
        kinds = {(a["kind"], a.get("gate_id") or a.get("field_id"))
                 for a in body["advisories"]}
        self.assertIn(("unsigned-gate", "informed-consent"), kinds)
        self.assertIn(("unsigned-gate", "irb-approval"), kinds)
        # sample records the received LOA, but no FDA authorization yet
        self.assertIn(("external-fact", "submission.fda_authorization_date"),
                      kinds)
        self.assertNotIn(("external-fact", "manufacturer.loa_received_date"),
                         kinds)
        # citations named on the advisories (312.60 / Part 50 / Part 56)
        blob = json.dumps(body["advisories"])
        self.assertIn("312.60", blob)
        self.assertIn("56.108", blob)
        # a refusal mutates NOTHING
        self.assertEqual(case, before)
        self.assertIsNone(case.get("enrollment"))
        self.assertEqual([r for r in case["audit"]
                          if r["action"] == "promote"], [])

    def test_non_emergency_canned_or_short_ack_refused(self):
        case = self._committed_case("p5badack")
        for bad in ("ok", "acknowledged",
                    "Recorded human act: skip the gates entirely please"):
            status, body = _http(
                "POST", "/api/case/p5badack/promote",
                {"actor": ENROLLER, "legal_basis": "authorization-164.508",
                 "acknowledge_unsigned_gates": bad})
            self.assertEqual(status, 400, bad)
            self.assertIn("own words", body["error"])
        self.assertIsNone(case.get("enrollment"))

    def test_non_emergency_own_words_ack_records_the_skip(self):
        case = self._committed_case("p5ackok")
        status, body = _http("POST", "/api/case/p5ackok/promote",
                             {"actor": ENROLLER,
                              "legal_basis": "authorization-164.508",
                              "acknowledge_unsigned_gates": ACK})
        self.assertEqual(status, 200, body)
        # persisted in the enrollment record — loud, not a silence
        enr = case["enrollment"]
        self.assertEqual(enr["acknowledge_unsigned_gates"], ACK)
        kinds = {(a["kind"], a.get("gate_id") or a.get("field_id"))
                 for a in enr["advisories"]}
        self.assertIn(("unsigned-gate", "informed-consent"), kinds)
        self.assertIn(("unsigned-gate", "irb-approval"), kinds)
        # ... and in the promote audit record's detail
        recs = [r for r in case["audit"] if r["action"] == "promote"]
        self.assertEqual(len(recs), 1)
        detail = recs[0]["detail"]
        self.assertEqual(detail["acknowledge_unsigned_gates"], ACK)
        self.assertIn("unsigned-gate:informed-consent", detail["advisories"])
        self.assertIn("unsigned-gate:irb-approval", detail["advisories"])
        self.assertIn("external-fact:submission.fda_authorization_date",
                      detail["advisories"])
        # ... and in the response
        self.assertTrue(body["advisories"])
        self.assertEqual(body["enrollment"]["advisories"], enr["advisories"])

    def test_non_emergency_signed_gates_promote_without_ack(self):
        case = self._committed_case("p5signed")
        self._sign_both_ethics_gates("p5signed")
        status, body = _http("POST", "/api/case/p5signed/promote",
                             {"actor": ENROLLER,
                              "legal_basis": "authorization-164.508"})
        self.assertEqual(status, 200, body)
        kinds = {a["kind"] for a in case["enrollment"]["advisories"]}
        self.assertNotIn("unsigned-gate", kinds)      # gates are signed
        self.assertIn("external-fact", kinds)         # FDA auth still absent
        self.assertIsNone(case["enrollment"]["acknowledge_unsigned_gates"])

    def test_emergency_route_is_advisory_only(self):
        # §50.23 / 56.104(c) reality: treatment may lawfully precede the
        # acts, so unsigned gates never refuse the emergency promote — but
        # the gaps are still recorded, loudly.
        case = self._committed_case("p5emerg", extra={
            "submission.emergency": "true",
            "submission.emergency_auth_datetime": "2026-06-26",
            "submission.first_treatment_date": "2026-07-06"})
        status, body = _http("POST", "/api/case/p5emerg/promote",
                             {"actor": ENROLLER,
                              "legal_basis": "treatment-disclosure"})
        self.assertEqual(status, 200, body)
        kinds = {(a["kind"], a.get("gate_id") or a.get("field_id"))
                 for a in case["enrollment"]["advisories"]}
        self.assertIn(("unsigned-gate", "informed-consent"), kinds)
        self.assertIn(("unsigned-gate", "irb-approval"), kinds)
        # emergency telephone authorization satisfies the FDA-auth fact
        self.assertNotIn(("external-fact", "submission.fda_authorization_date"),
                         kinds)

    def test_recorded_fda_authorization_clears_that_advisory(self):
        case = self._committed_case("p5fdaauth", extra={
            "submission.fda_authorization_date": "2026-07-01"})
        self._sign_both_ethics_gates("p5fdaauth")
        status, _ = _http("POST", "/api/case/p5fdaauth/promote",
                          {"actor": ENROLLER,
                           "legal_basis": "authorization-164.508"})
        self.assertEqual(status, 200)
        self.assertEqual(case["enrollment"]["advisories"], [])


# ---------------------------------------------------------------------------
# M4 (render) — escalate-only advisory lines in the check ledger
# ---------------------------------------------------------------------------

class TestCheckLedgerAdvisories(P5TestBase):

    def test_advisories_render_as_notes_never_status_changes(self):
        case = self._committed_case("p5check")
        before = server._check_payload(case)
        before_by_doc = {i["doc_id"]: i for i in before["ledger"]}
        self.assertEqual(before["enrollment_advisories"], [])
        status, _ = _http("POST", "/api/case/p5check/promote",
                          {"actor": ENROLLER,
                           "legal_basis": "authorization-164.508",
                           "acknowledge_unsigned_gates": ACK})
        self.assertEqual(status, 200)
        after = server._check_payload(case)
        self.assertTrue(after["enrollment_advisories"])
        gate_rows = [i for i in after["ledger"]
                     if i["gate_id"] in ("informed-consent", "irb-approval")]
        self.assertTrue(gate_rows)
        for row in gate_rows:
            # P7 (m2): physician-facing vocabulary is "treatment start".
            self.assertTrue(
                any("TREATMENT-START ADVISORY" in n for n in row["notes"]),
                row)
            # escalate-only: a note, never a demotion or a promotion
            self.assertEqual(row["status"],
                             before_by_doc[row["doc_id"]]["status"])


# ---------------------------------------------------------------------------
# M13 — own-words statements + evidence on the ethics gates
# ---------------------------------------------------------------------------

class TestSignoffOwnWords(P5TestBase):

    def test_statement_required_for_ethics_gates(self):
        case = self._committed_case("p5sostmt")
        status, body = self._signoff("p5sostmt", "informed-consent", ICF_DOC,
                                     "investigator")
        self.assertEqual(status, 400)
        self.assertIn("own words", body["error"])
        self.assertEqual(case["signoffs"], [])
        self.assertEqual([r for r in case["audit"]
                          if r["action"] == "signoff"], [])

    def test_short_and_placeholder_statements_refused(self):
        self._committed_case("p5sobad")
        for bad in ("I consent.",
                    "Recorded human act: performed outside OSSICRO today ok"):
            status, body = self._signoff("p5sobad", "informed-consent",
                                         ICF_DOC, "investigator", bad)
            self.assertEqual(status, 400, bad)
            self.assertIn("own words", body["error"])

    def test_own_words_and_evidence_persisted(self):
        case = self._committed_case("p5sook")
        status, body = self._signoff(
            "p5sook", "irb-approval", IRB_DOC, "irb", IRB_STATEMENT,
            {"concurrence_date": "2026-07-08",
             "concurring_member": "Dr. P. Mfume (chair)",
             "irb_reference": "MRB-2026-114"},
            signer="Alex B. Chen, MD")
        self.assertEqual(status, 200, body)
        rec = case["signoffs"][-1]
        self.assertEqual(rec["statement"], IRB_STATEMENT)
        self.assertEqual(rec["evidence"], {
            "concurrence_date": "2026-07-08",
            "concurring_member": "Dr. P. Mfume (chair)",
            "irb_reference": "MRB-2026-114"})
        # audit carries the KEYS, never the values (INV-8)
        arec = [r for r in case["audit"] if r["action"] == "signoff"][-1]
        self.assertEqual(arec["detail"]["evidence_keys"],
                         ["concurrence_date", "concurring_member",
                          "irb_reference"])
        self.assertNotIn("MRB-2026-114", json.dumps(case["audit"]))

    def test_evidence_keys_asked_even_when_blank(self):
        case = self._committed_case("p5soblank")
        status, _ = self._signoff("p5soblank", "informed-consent", ICF_DOC,
                                  "investigator", CONSENT_STATEMENT,
                                  evidence={})
        self.assertEqual(status, 200)
        rec = case["signoffs"][-1]
        self.assertEqual(rec["evidence"], {"consent_date": ""})   # honest blank

    def test_other_gates_keep_the_synthesized_statement_path(self):
        case = self._committed_case("p5soother")
        status, _ = self._signoff(
            "p5soother", "submission-to-fda",
            "form-fda-3926-individual-patient-expanded-access",
            "sponsor-investigator")
        self.assertEqual(status, 200)
        self.assertEqual(case["signoffs"][-1]["statement"], "")
        self.assertNotIn("evidence", case["signoffs"][-1])

    def test_own_words_signoff_still_moves_ledger_amber_to_green(self):
        # The stored own-words statement must survive the engine re-apply
        # (gates.record_signoff) that turns amber to green.
        case = self._committed_case("p5sogreen")
        payload = server._check_payload(case)
        item = [i for i in payload["ledger"] if i["doc_id"] == ICF_DOC][0]
        self.assertEqual(item["status"], "amber")
        self._signoff("p5sogreen", "informed-consent", ICF_DOC,
                      "investigator", CONSENT_STATEMENT,
                      {"consent_date": "2026-07-07"})
        payload = server._check_payload(case)
        item = [i for i in payload["ledger"] if i["doc_id"] == ICF_DOC][0]
        self.assertEqual(item["status"], "green")


# ---------------------------------------------------------------------------
# m13b — supersede, never overwrite
# ---------------------------------------------------------------------------

class TestSignoffSupersede(P5TestBase):

    def test_rerecord_supersedes_and_keeps_history(self):
        case = self._committed_case("p5super")
        self._signoff("p5super", "informed-consent", ICF_DOC, "investigator",
                      CONSENT_STATEMENT, {"consent_date": "2026-07-07"})
        status, _ = self._signoff(
            "p5super", "informed-consent", ICF_DOC, "investigator",
            "I re-obtained consent after the revised risk information.",
            {"consent_date": "2026-07-09"}, signer="Dana Q. Osei, MD",
            date="2026-07-09")
        self.assertEqual(status, 200)
        self.assertEqual(len(case["signoffs"]), 2)   # history kept (11.10(e))
        old, new = case["signoffs"]
        self.assertTrue(old["superseded_at"])
        self.assertEqual(old["superseded_by"], "Dana Q. Osei, MD")
        self.assertNotIn("superseded_at", new)
        # validity reads only the active record
        active = server._active_signoffs(case)
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["signer_name"], "Dana Q. Osei, MD")
        # audit records the supersede count on the second act
        arecs = [r for r in case["audit"] if r["action"] == "signoff"]
        self.assertEqual(arecs[0]["detail"]["superseded_prior"], 0)
        self.assertEqual(arecs[1]["detail"]["superseded_prior"], 1)

    def test_check_payload_lists_only_the_active_record(self):
        case = self._committed_case("p5superchk")
        self._signoff("p5superchk", "informed-consent", ICF_DOC,
                      "investigator", CONSENT_STATEMENT,
                      {"consent_date": "2026-07-07"})
        self._signoff("p5superchk", "informed-consent", ICF_DOC,
                      "investigator",
                      "I repeated the consent conversation and re-signed.",
                      {"consent_date": "2026-07-09"},
                      signer="Dana Q. Osei, MD", date="2026-07-09")
        payload = server._check_payload(case)
        listed = [s for s in payload["signoffs"]
                  if s["gate_id"] == "informed-consent"]
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["signer_name"], "Dana Q. Osei, MD")
        # the gate still clears from the active record
        item = [i for i in payload["ledger"] if i["doc_id"] == ICF_DOC][0]
        self.assertEqual(item["status"], "green")


if __name__ == "__main__":
    unittest.main(verbosity=2)
