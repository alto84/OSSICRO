"""Overhaul P7 — obligations lifecycle: complete, decoupled from promote,
treatment vocabulary.

Covers:
  - M11: the sponsor-obligations checklist is DECOUPLED from promote — rows
    appear as soon as ANY anchoring fact exists (submission.emergency_auth_
    datetime, submission.first_treatment_date, submission.fda_receipt_date,
    treatment.conclusion_date) or an enrollment record does. Promote remains
    only the HIPAA-basis transition it actually is. A case with neither an
    anchoring fact nor an enrollment record honestly shows [].
  - M10: the always-present 21 CFR 312.310(c)(2) end-of-treatment written-
    summary row — armed from treatment.conclusion_date with the due date
    being the conclusion date ITSELF (due "at the conclusion", never
    date+N); honestly UNARMED with the resolving question until recorded;
    unreadable date -> the unreadable-date question, never a guess (HC3).
  - Tracked-subset disclosure: every checklist payload carries the one-line
    disclosure that the list is the tracked subset of the sponsor-
    investigator's duties, not the entirety.
  - m2: physician-facing vocabulary is "treatment start"; the INV-5
    machinery (endpoint, enrollment record/JSON keys, audit action names)
    and the patient-page strings are UNCHANGED.

Socketless in-process requests through the REAL Handler — no port is ever
bound (the live UI-QA server on 8765 is never touched).
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

from ossicro.review_port import DeterministicStubReviewer   # noqa: E402

ACTOR = "Jordan A. Rivera, MD"
ENROLLER = "Priya N. Kapoor, MD"

ACK = ("I am recording this treatment start before the consent and IRB "
       "sign-offs are recorded; both acts remain mine to perform.")

# The M11 anchoring facts — mirrors server._OBLIGATION_ANCHOR_FIELDS.
ANCHOR_FIELDS = (
    "submission.emergency_auth_datetime",
    "submission.first_treatment_date",
    "submission.fda_receipt_date",
    "treatment.conclusion_date",
)

CONCLUSION_CITATION = "21 CFR 312.310(c)(2)"

INDEX_HTML = os.path.join(APP_DIR, "static", "index.html")


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


class P7TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p7-tests-")
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

    def _case_with(self, case_id, extra=None, drop_anchors=False):
        """A registered case with the sample intake; anchors can be dropped
        (the sample fixture records submission.fda_receipt_date) and extras
        applied. Uncommitted — M11 needs no commit for visibility."""
        case = server._new_case()
        fields = dict(server._sample_payload()["fields"])
        if drop_anchors:
            for f in ANCHOR_FIELDS:
                fields.pop(f, None)
        for key, value in (extra or {}).items():
            if value is None:
                fields.pop(key, None)
            else:
                fields[key] = value
        _write_intake(case, fields)
        return self._register(case_id, case)

    def _committed(self, case):
        body, status = server._profile_commit(case, {"actor": ACTOR})
        assert status == 200, body
        return case

    def _promote_ok(self, case_id, legal_basis="authorization-164.508"):
        status, body = _http("POST", "/api/case/%s/promote" % case_id,
                             {"actor": ENROLLER, "legal_basis": legal_basis,
                              "acknowledge_unsigned_gates": ACK})
        self.assertEqual(status, 200, body)
        return body


# ---------------------------------------------------------------------------
# M11 — decoupled from promote: anchored-or-enrolled makes the list visible
# ---------------------------------------------------------------------------

class TestDecoupledFromPromote(P7TestBase):

    def test_no_anchor_no_enrollment_is_honestly_empty(self):
        self._case_with("p7empty", drop_anchors=True)
        status, got = _http("GET", "/api/case/p7empty")
        self.assertEqual(status, 200)
        self.assertIsNone(got["enrollment"])
        self.assertEqual(got["obligations"], [])

    def test_receipt_date_alone_surfaces_checklist_pre_promote(self):
        # The sample fixture's fda_receipt_date is an anchoring fact: the
        # checklist appears with NO enrollment record and NO commit.
        self._case_with("p7anchor")
        status, got = _http("GET", "/api/case/p7anchor")
        self.assertEqual(status, 200)
        self.assertIsNone(got["enrollment"])
        self.assertEqual(got["mode"], "PREPARATORY_REVIEW")
        obligations = got["obligations"]
        self.assertEqual(len(obligations), 6)
        by = {o["citation"]: o for o in obligations}
        self.assertTrue(by["21 CFR 312.33"]["armed"])   # armed from receipt
        # Everything else stays honestly unarmed pre-promote.
        for citation, o in by.items():
            if citation != "21 CFR 312.33":
                self.assertFalse(o["armed"], citation)
                self.assertIsNone(o["due"], citation)
                self.assertTrue(o["resolving_question"], citation)

    def test_each_anchor_field_alone_surfaces_the_checklist(self):
        for i, field in enumerate(ANCHOR_FIELDS):
            case_id = "p7one%d" % i
            self._case_with(case_id, drop_anchors=True,
                            extra={field: "2026-07-06"})
            status, got = _http("GET", "/api/case/%s" % case_id)
            self.assertEqual(status, 200)
            self.assertIsNone(got["enrollment"])
            self.assertEqual(len(got["obligations"]), 6, field)

    def test_promote_without_anchors_still_surfaces_checklist(self):
        # The enrollment record remains a visibility trigger of its own:
        # promote is still the HIPAA-basis transition, and the duties it
        # names stay in view even when no anchor date has been recorded.
        case = self._case_with("p7bare", drop_anchors=True)
        self._committed(case)
        body = self._promote_ok("p7bare")
        checklist = body["obligations_checklist"]
        self.assertEqual(len(checklist), 6)
        for o in checklist:   # nothing armed: no anchor date exists (HC3)
            self.assertFalse(o["armed"])
            self.assertIsNone(o["due"])
            self.assertTrue(o["resolving_question"])

    def test_promote_remains_the_hipaa_transition_only(self):
        # M11: pre-promote visibility does not blur the transition — mode
        # stays PREPARATORY_REVIEW and enrollment stays None until the act.
        case = self._case_with("p7trans")
        status, got = _http("GET", "/api/case/p7trans")
        self.assertEqual(got["mode"], "PREPARATORY_REVIEW")
        self.assertIsNone(got["enrollment"])
        self.assertTrue(got["obligations"])   # visible all the same
        self._committed(case)
        self._promote_ok("p7trans")
        status, got = _http("GET", "/api/case/p7trans")
        self.assertEqual(got["mode"], "ENROLLMENT")
        self.assertTrue(got["enrollment"])


# ---------------------------------------------------------------------------
# M10 — the 312.310(c)(2) end-of-treatment summary row
# ---------------------------------------------------------------------------

class TestConclusionSummaryRow(P7TestBase):

    def _row(self, case_id):
        status, got = _http("GET", "/api/case/%s" % case_id)
        self.assertEqual(status, 200)
        rows = [o for o in got["obligations"]
                if o["citation"] == CONCLUSION_CITATION]
        self.assertEqual(len(rows), 1)
        return rows[0]

    def test_always_present_and_unarmed_until_conclusion_recorded(self):
        self._case_with("p7concl0")   # receipt anchor only; no conclusion
        row = self._row("p7concl0")
        self.assertFalse(row["armed"])
        self.assertIsNone(row["due"])
        self.assertEqual(row["trigger_field"], "treatment.conclusion_date")
        self.assertIn("treatment-conclusion date", row["resolving_question"])
        self.assertIn("treatment.conclusion_date", row["resolving_question"])
        self.assertIn(CONCLUSION_CITATION, row["resolving_question"])
        self.assertIn("never assumes an end date", row["resolving_question"])

    def test_armed_due_is_the_conclusion_date_itself_not_date_plus_n(self):
        self._case_with("p7concl1",
                        extra={"treatment.conclusion_date": "2026-12-15"})
        row = self._row("p7concl1")
        self.assertTrue(row["armed"])
        self.assertEqual(row["due"], "2026-12-15")   # AT the conclusion
        self.assertIsNone(row["days"])               # no +N convention
        self.assertEqual(row["basis"], "at-conclusion")
        self.assertEqual(row["owner"], "physician-sponsor")
        self.assertIsNone(row["resolving_question"])
        self.assertIn("Written summary", row["obligation"])
        self.assertIn("adverse effects", row["obligation"])
        self.assertIn("conclusion of treatment", row["obligation"])

    def test_unreadable_conclusion_date_is_unarmed_never_guessed(self):
        self._case_with("p7conclbad",
                        extra={"treatment.conclusion_date": "next winter"})
        row = self._row("p7conclbad")
        self.assertFalse(row["armed"])
        self.assertIsNone(row["due"])
        self.assertIn("could not be read", row["resolving_question"])

    def test_row_survives_promote_and_arms_later(self):
        # The tracker and the generated treatment plan's 312.310(c)(2)
        # promise agree across the whole lifecycle: present at promote,
        # armed the moment the conclusion date is recorded.
        case = self._case_with("p7concl2")
        self._committed(case)
        body = self._promote_ok("p7concl2")
        rows = [o for o in body["obligations_checklist"]
                if o["citation"] == CONCLUSION_CITATION]
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["armed"])
        status, _ = _http("POST", "/api/case/p7concl2/intake",
                          {"fields": {"treatment.conclusion_date": "2027-01-31"},
                           "actor": ENROLLER})
        self.assertEqual(status, 200)
        row = self._row("p7concl2")
        self.assertTrue(row["armed"])
        self.assertEqual(row["due"], "2027-01-31")


# ---------------------------------------------------------------------------
# Tracked-subset disclosure — the checklist never reads as the entirety
# ---------------------------------------------------------------------------

class TestTrackedSubsetDisclosure(P7TestBase):

    def test_case_payload_carries_the_disclosure(self):
        self._case_with("p7subset")
        status, got = _http("GET", "/api/case/p7subset")
        self.assertEqual(status, 200)
        note = got["obligations_note"]
        self.assertIn("tracked subset", note)
        self.assertIn("not", note)
        self.assertIn("entirety", note)
        self.assertIn("312.57", note)
        self.assertIn("312.62", note)
        self.assertIn("untracked", note)

    def test_promote_response_carries_the_disclosure(self):
        case = self._case_with("p7subset2")
        self._committed(case)
        body = self._promote_ok("p7subset2")
        self.assertEqual(body["obligations_note"],
                         server.STRINGS["obligations_tracked_subset"])

    def test_ui_renders_the_disclosure_and_the_new_wording(self):
        with open(INDEX_HTML, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("tracked subset of sponsor-investigator duties", html)
        # The M11 reword: shown from the moment the anchoring facts are
        # recorded — replacing "duties the enrollment creates".
        self.assertIn("shown from the moment the anchoring facts are recorded",
                      html)
        self.assertNotIn("duty the enrollment creates", html)


# ---------------------------------------------------------------------------
# m2 — treatment-start vocabulary; machinery and patient strings unchanged
# ---------------------------------------------------------------------------

class TestTreatmentVocabulary(P7TestBase):

    def test_physician_strings_say_treatment_start(self):
        self.assertIn("Treatment start recorded",
                      server.STRINGS["promote_note"])
        self.assertNotIn("Enrollment recorded",
                         server.STRINGS["promote_note"])
        self.assertIn("treatment-start record stands",
                      server.STRINGS["promote_already_enrolled"])
        self.assertIn("start of treatment",
                      server.STRINGS["promote_actor_required"])
        self.assertIn("TREATMENT-START ADVISORY",
                      server.STRINGS["promote_advisory_unsigned_gate"])
        self.assertIn("TREATMENT-START ADVISORY",
                      server.STRINGS["promote_advisory_external_fact"])

    def test_ui_physician_workspace_renamed_patient_page_untouched(self):
        with open(INDEX_HTML, encoding="utf-8") as f:
            html = f.read()
        # The physician-facing act is renamed exactly as specified.
        self.assertIn("Record start of treatment (legal basis)", html)
        self.assertNotIn('btn: "Record enrollment"', html)
        # The promote card asks for the 56.104(c) trigger right there (M1).
        self.assertIn("submission.first_treatment_date", html)
        self.assertIn("enTreatDate", html)
        # Patient-page strings are deliberately UNCHANGED.
        self.assertIn("Your enrollment has been recorded", html)

    def test_server_patient_strings_unchanged(self):
        # The patient persona keeps its own plain-language wording.
        self.assertIn("enrolled", server.STRINGS["patient_stage_enrolled"])

    def test_audit_action_names_and_machinery_unchanged(self):
        case = self._case_with("p7audit")
        self._committed(case)
        self._promote_ok("p7audit")
        recs = [r for r in case["audit"] if r["action"] == "promote"]
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["target"], "enrollment")
        self.assertEqual(recs[0]["detail"]["to_mode"], "ENROLLMENT")
        # The endpoint and the record keys are untouched machinery.
        self.assertIn("enrollment", case)
        status, got = _http("GET", "/api/case/p7audit")
        self.assertEqual(status, 200)
        self.assertIn("enrollment", got)
        self.assertIn("obligations", got)


if __name__ == "__main__":   # pragma: no cover
    unittest.main()
