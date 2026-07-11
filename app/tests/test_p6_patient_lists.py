"""Overhaul P6 — app half: patient remaining-lists per route (m9), the
post-enrollment voluntariness line (m10), and the fix-loop reachability of
the EA consent form's intake fields (M3 plumbing).

Covers:
  - m9: the three ``patient_remaining_*`` lists (draft / committed /
    released) have EMERGENCY variants keyed on the recorded
    ``submission.emergency`` flag — the standard lists would be false on the
    emergency route (phone authorization, after-the-fact IRB notice,
    possible consent exception). Plain-language register preserved: the
    patient view stays jargon-free either way.
  - m10: ``patient_remaining_enrolled`` carries the voluntariness line —
    the 50.25(a)(8) thread does not end at enrollment.
  - M3: a ledger question naming ``injury_compensation_statement`` /
    ``cost_statement`` maps to the P2 intake fields through the fix-loop
    (ea_generators.ICF_EA_FIELD_SOURCES is consumed by the span map).
  - The check ledger carries the EA ICF doc id for a committed sample case.

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
LINKER = "Priya N. Kapoor, MD"

EA_ICF = "informed-consent-form-part50-ea"

# The patient view must never leak regulatory jargon (Wave-4 guarantee,
# extended to the new emergency variants).
JARGON = ("312.", "CFR", "IND ", "LOA", "sponsor-investigator", "50.23")


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


class P6TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-p6-tests-")
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

    def _sample_case(self, extra=None):
        case = server._new_case()
        fields = dict(server._sample_payload()["fields"])
        if extra:
            fields.update(extra)
        _write_intake(case, fields)
        return case


# ---------------------------------------------------------------------------
# m9 — emergency variants of the three remaining-lists, keyed on the route
# ---------------------------------------------------------------------------

class TestEmergencyRemainingLists(P6TestBase):

    STAGES = ("draft", "committed", "released")

    def test_the_three_lists_have_emergency_variants(self):
        for stage in self.STAGES:
            std = server.STRINGS["patient_remaining_" + stage]
            em = server.STRINGS["patient_remaining_%s_emergency" % stage]
            self.assertTrue(em, stage)
            self.assertNotEqual(em, std, stage)
            joined = " ".join(em)
            # The emergency reality, in plain language: phone permission,
            # after-the-fact ethics-board notice, consent whenever possible.
            self.assertIn("by\nphone".replace("\n", " "), joined, stage)
            self.assertIn("instead of approving it\nfirst".replace("\n", " "),
                          joined, stage)
            self.assertIn("your choice", joined, stage)

    def test_no_emergency_variant_claims_fda_must_allow_first(self):
        # The standard lists' "The FDA must allow the treatment to go ahead."
        # is exactly what is NOT true pre-written-submission on the
        # emergency route.
        for stage in self.STAGES:
            em = server.STRINGS["patient_remaining_%s_emergency" % stage]
            self.assertNotIn("The FDA must allow the treatment to go ahead.",
                             em, stage)
            self.assertNotIn("An ethics review board (called an IRB) must "
                             "agree.", em, stage)

    def test_patient_view_picks_the_variant_from_the_recorded_flag(self):
        for flag, expect_emergency in (("true", True), ("false", False)):
            case = self._sample_case({"submission.emergency": flag})
            view = server._patient_view(case)
            expected = server.STRINGS[
                "patient_remaining_draft_emergency" if expect_emergency
                else "patient_remaining_draft"]
            self.assertEqual(view["what_remains"], list(expected), flag)

    def test_variant_tracks_stage_transitions(self):
        # Unit-level: _case_stage keys on the enrollment/released/committed
        # markers; the emergency variant must follow the stage.
        case = self._register("p6stages",
                              self._sample_case({"submission.emergency": "true"}))
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 200, body)
        view = server._patient_view(case)
        self.assertEqual(view["stage"], "committed")
        self.assertEqual(view["what_remains"],
                         list(server.STRINGS["patient_remaining_committed_emergency"]))
        case["released"] = {"actor": ACTOR}          # stage marker (dict)
        view = server._patient_view(case)
        self.assertEqual(view["stage"], "released")
        self.assertEqual(view["what_remains"],
                         list(server.STRINGS["patient_remaining_released_emergency"]))

    def test_emergency_view_stays_plain_language_over_http(self):
        case = self._register("p6emview",
                              self._sample_case({"submission.emergency": "true"}))
        _status, body = _http("POST", "/api/case/p6emview/patient-link",
                              {"actor": LINKER})
        status, view = _http("GET", "/api/patient/%s" % body["patient_token"])
        self.assertEqual(status, 200)
        text = json.dumps(view)
        for jargon in JARGON:
            self.assertNotIn(jargon, text, jargon)
        self.assertEqual(view["what_remains"],
                         list(server.STRINGS["patient_remaining_draft_emergency"]))

    def test_standard_lists_unchanged_for_non_emergency(self):
        case = self._sample_case()          # sample is non-emergency
        view = server._patient_view(case)
        self.assertEqual(view["what_remains"],
                         list(server.STRINGS["patient_remaining_draft"]))


# ---------------------------------------------------------------------------
# m10 — the voluntariness line survives enrollment
# ---------------------------------------------------------------------------

class TestEnrolledVoluntariness(P6TestBase):

    def test_enrolled_list_carries_the_voluntariness_line(self):
        lines = server.STRINGS["patient_remaining_enrolled"]
        joined = " ".join(lines)
        self.assertIn("continuing is your choice", joined)
        self.assertIn("stop at any time", joined)

    def test_enrolled_view_renders_it(self):
        case = self._register("p6enr", self._sample_case())
        case["enrollment"] = {"legal_basis": "authorization-164.508"}
        view = server._patient_view(case)
        self.assertEqual(view["stage"], "enrolled")
        self.assertTrue(any("continuing is your choice" in line
                            for line in view["what_remains"]))
        for jargon in JARGON:
            self.assertNotIn(jargon, json.dumps(view["what_remains"]), jargon)


# ---------------------------------------------------------------------------
# M3 plumbing — the EA consent fields are reachable by the fix-loop
# ---------------------------------------------------------------------------

class TestConsentFixLoop(P6TestBase):

    def test_ledger_questions_map_to_the_p2_intake_fields(self):
        for span, field_id in (
                ("injury_compensation_statement",
                 "consent.injury_compensation_statement"),
                ("cost_statement", "consent.cost_statement"),
                ("consent_duration", "consent.duration")):
            q = "Provide '%s' for the document (required by its authority)." % span
            self.assertEqual(server._field_id_for_question(q), field_id, span)

    def test_span_map_consumes_the_exported_ea_icf_table(self):
        from ossicro.ea_generators import ICF_EA_FIELD_SOURCES
        for span, (path, _citation) in ICF_EA_FIELD_SOURCES.items():
            if path in server.SCHEMA_FIELDS:
                self.assertEqual(server.SPAN_TO_FIELD.get(span), path, span)

    def test_check_ledger_carries_the_ea_icf(self):
        case = self._register("p6ledger", self._sample_case())
        payload = server._check_payload(case)
        by_doc = {i["doc_id"]: i for i in payload["ledger"]}
        self.assertIn(EA_ICF, by_doc)
        self.assertNotIn("informed-consent-form-part50", by_doc)
        # amber: complete but awaiting the non-delegable consent event
        self.assertEqual(by_doc[EA_ICF]["status"], "amber")

    def test_missing_a6_yields_red_with_fixable_question(self):
        case = self._register("p6a6", self._sample_case(
            {"consent.injury_compensation_statement": ""}))
        payload = server._check_payload(case)
        item = next(i for i in payload["ledger"] if i["doc_id"] == EA_ICF)
        self.assertEqual(item["status"], "red")
        # The check payload's questions are fix-loop-resolved dicts: the
        # ledger question DIRECTS to the new intake field (M3).
        question = next(q for q in item["questions"]
                        if "injury_compensation_statement" in q["text"])
        self.assertEqual(question["field_id"],
                         "consent.injury_compensation_statement")


if __name__ == "__main__":
    unittest.main(verbosity=2)
