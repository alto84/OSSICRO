"""Wave-4 app tests: patient persona (tokenized) + INV-5 promote() + CRO board.

Covers:
  - the patient view is reachable ONLY via the opaque minted token: a bad
    token (including the case_id itself) is a bare 404 with no enumeration
    surface and no not-found vs not-authorized distinction;
  - POST /patient-link is a NAMED, audit-logged act ('patient_link'); the
    token is minted once and stable across re-shares;
  - the patient view is READ-ONLY plain language: no case_id, no clinical
    PHI beyond the coded id + drug name, the standing draft notice always
    present, and the stage tracks draft -> committed -> released -> enrolled;
  - INV-5 promote() requires a committed profile (409), a named actor (400),
    and a recognized legal_basis (400); on success it records the enrollment
    block (actor/at/legal_basis/from_hash), flips mode to ENROLLMENT, writes
    EXACTLY ONE 'promote' audit record with the hash chain intact, and emits
    the obligations checklist with citations — armed only from recorded
    anchor dates, honestly UNARMED with a resolving question otherwise (HC3:
    never a fabricated date). A repeat promote is refused;
  - GET /api/cro/board is READ-ONLY (no POST route), reflects each case's
    stage / profile state / gate + ledger rollups / released + enrolled
    flags, and never mutates a case.

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
LINKER = "Dana Q. Osei, MD"
ENROLLER = "Priya N. Kapoor, MD"

LEGAL_BASES = ("authorization-164.508", "waiver-164.512", "treatment-disclosure")


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
# Socketless in-process HTTP (same harness as test_wave3_pdf_release.py).
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


class Wave4TestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-wave4-tests-")
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

    def _sample_case(self, extra=None):
        case = server._new_case()
        fields = dict(server._sample_payload()["fields"])
        if extra:
            fields.update(extra)
        _write_intake(case, fields)
        return case

    def _committed_case(self, case_id, extra=None):
        case = self._register(case_id, self._sample_case(extra))
        body, status = server._profile_commit(case, {"actor": ACTOR})
        assert status == 200, body
        return case

    def _promote_ok(self, case_id, legal_basis="authorization-164.508"):
        status, body = _http("POST", "/api/case/%s/promote" % case_id,
                             {"actor": ENROLLER, "legal_basis": legal_basis})
        self.assertEqual(status, 200, body)
        return body


# ---------------------------------------------------------------------------
# Patient persona — token minting (a named, audited act)
# ---------------------------------------------------------------------------

class TestPatientLink(Wave4TestBase):

    def test_link_requires_named_actor(self):
        case = self._register("w4linknoactor", self._sample_case())
        status, body = _http("POST", "/api/case/w4linknoactor/patient-link",
                             {"actor": "   "})
        self.assertEqual(status, 400)
        self.assertIn("actor", body["error"])
        self.assertIsNone(case["patient_token"])
        self.assertEqual(
            [r for r in case["audit"] if r["action"] == "patient_link"], [])

    def test_link_mints_opaque_token_and_audits(self):
        case = self._register("w4linkmint", self._sample_case())
        status, body = _http("POST", "/api/case/w4linkmint/patient-link",
                             {"actor": LINKER})
        self.assertEqual(status, 200)
        token = body["patient_token"]
        self.assertEqual(len(token), 32)                 # uuid4().hex — opaque
        self.assertNotIn("w4linkmint", token)            # never the case_id
        self.assertEqual(body["link"], "/api/patient/%s" % token)
        self.assertEqual(case["patient_token"], token)
        recs = [r for r in case["audit"] if r["action"] == "patient_link"]
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["actor"], LINKER)
        self.assertEqual(recs[0]["target"], "patient-view")
        self.assertEqual(recs[0]["detail"], {"minted": True})
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])

    def test_reshare_returns_same_token_and_audits_again(self):
        case = self._register("w4linkagain", self._sample_case())
        _, first = _http("POST", "/api/case/w4linkagain/patient-link",
                         {"actor": LINKER})
        _, second = _http("POST", "/api/case/w4linkagain/patient-link",
                          {"actor": ACTOR})
        self.assertEqual(first["patient_token"], second["patient_token"])
        recs = [r for r in case["audit"] if r["action"] == "patient_link"]
        self.assertEqual(len(recs), 2)                   # every share is an act
        self.assertEqual(recs[1]["detail"], {"minted": False})
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])

    def test_unknown_case_404(self):
        status, _ = _http("POST", "/api/case/nosuchcase42/patient-link",
                          {"actor": LINKER})
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# Patient persona — the read-only view behind the token
# ---------------------------------------------------------------------------

class TestPatientView(Wave4TestBase):

    def _minted(self, case_id, case):
        _, body = _http("POST", "/api/case/%s/patient-link" % case_id,
                        {"actor": LINKER})
        return body["patient_token"]

    def test_bad_token_is_bare_404_no_enumeration(self):
        case = self._register("w4viewbadtok", self._sample_case())
        self._minted("w4viewbadtok", case)
        for bad in ("deadbeefdeadbeefdeadbeefdeadbeef",  # well-formed, wrong
                    "w4viewbadtok",                      # the case_id itself
                    "x"):
            status, body = _http("GET", "/api/patient/%s" % bad)
            self.assertEqual(status, 404)
            self.assertEqual(body, {"error": "not found"})  # nothing to probe

    def test_unminted_case_unreachable_even_with_no_token(self):
        # A case whose link was never minted has NO patient surface at all.
        self._register("w4viewunmint", self._sample_case())
        status, body = _http("GET", "/api/patient/None")
        self.assertEqual(status, 404)
        status, body = _http("GET", "/api/patient/w4viewunmint")
        self.assertEqual(status, 404)

    def test_view_is_plain_language_and_carries_no_case_id_or_phi(self):
        case = self._register("w4viewclean", self._sample_case())
        token = self._minted("w4viewclean", case)
        status, headers, raw = _http_raw("GET", "/api/patient/%s" % token)
        self.assertEqual(status, 200)
        body = json.loads(raw.decode("utf-8"))
        text = raw.decode("utf-8")
        # No case_id anywhere in the serialized payload.
        self.assertNotIn("w4viewclean", text)
        self.assertNotIn("case_id", body)
        # No clinical PHI beyond what the patient already holds: the
        # diagnosis narrative must NOT appear; coded id + drug name may.
        self.assertNotIn("cholangiocarcinoma", text)
        self.assertNotIn(case["intake"]["patient.diagnosis"], text)
        self.assertEqual(body["patient_coded_id"], "PT-3926-014")
        self.assertEqual(body["drug"], "Cytoravir")
        # The standing notice: a draft, nothing submitted to the FDA.
        self.assertIn("DRAFT", body["notice"])
        self.assertIn("Nothing has been submitted to the FDA", body["notice"])
        self.assertTrue(body["draft"])
        # Plain-language stage + what-remains, no regulatory jargon.
        self.assertEqual(body["stage"], "draft")
        self.assertTrue(body["status"])
        self.assertTrue(body["what_remains"])
        for jargon in ("312.", "CFR", "IND ", "LOA", "sponsor-investigator"):
            self.assertNotIn(jargon, text)

    def test_view_never_mutates_case(self):
        case = self._register("w4viewnomut", self._sample_case())
        token = self._minted("w4viewnomut", case)
        before = copy.deepcopy({k: v for k, v in case.items() if k != "audit"})
        _http("GET", "/api/patient/%s" % token)
        after = {k: v for k, v in case.items() if k != "audit"}
        self.assertEqual(after, before)

    def test_stage_tracks_lifecycle(self):
        case = self._register("w4viewstages", self._sample_case())
        token = self._minted("w4viewstages", case)

        def stage():
            status, body = _http("GET", "/api/patient/%s" % token)
            self.assertEqual(status, 200)
            # MAJOR-2: the "nothing submitted" notice is correct in
            # draft/committed/released, but false once enrolled — so the
            # enrolled stage must NOT carry it.
            if body["stage"] == "enrolled":
                self.assertNotIn("Nothing has been submitted to the FDA",
                                 body["notice"])
                self.assertIn("doctor's office", body["notice"])
            else:
                self.assertIn("Nothing has been submitted to the FDA",
                              body["notice"])
            return body["stage"]

        self.assertEqual(stage(), "draft")
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 200, body)
        self.assertEqual(stage(), "committed")
        server._generate_payload(case)
        status, _ = _http("POST", "/api/case/w4viewstages/release",
                          {"actor": LINKER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        self.assertEqual(stage(), "released")
        self._promote_ok("w4viewstages")
        self.assertEqual(stage(), "enrolled")


# ---------------------------------------------------------------------------
# INV-5 promote() — the preparatory-review -> enrollment legal transition
# ---------------------------------------------------------------------------

class TestPromote(Wave4TestBase):

    def test_requires_named_actor(self):
        case = self._committed_case("w4pronoactor")
        status, body = _http("POST", "/api/case/w4pronoactor/promote",
                             {"actor": "  ", "legal_basis": LEGAL_BASES[0]})
        self.assertEqual(status, 400)
        self.assertIn("actor", body["error"])
        self.assertIsNone(case["enrollment"])
        self.assertEqual(
            [r for r in case["audit"] if r["action"] == "promote"], [])

    def test_requires_recognized_legal_basis(self):
        case = self._committed_case("w4probasis")
        for bad in ({}, {"legal_basis": ""}, {"legal_basis": "vibes"},
                    {"legal_basis": "164.508"}):
            payload = {"actor": ENROLLER}
            payload.update(bad)
            status, body = _http("POST", "/api/case/w4probasis/promote", payload)
            self.assertEqual(status, 400)
            self.assertIn("legal_basis", body["error"])
            self.assertEqual(sorted(body["allowed"]), sorted(LEGAL_BASES))
        self.assertIsNone(case["enrollment"])
        self.assertEqual(case.get("mode"), "PREPARATORY_REVIEW")

    def test_requires_committed_profile(self):
        case = self._register("w4prouncommit", self._sample_case())
        status, body = _http("POST", "/api/case/w4prouncommit/promote",
                             {"actor": ENROLLER, "legal_basis": LEGAL_BASES[0]})
        self.assertEqual(status, 409)
        self.assertEqual(body["error"], "profile not committed")
        self.assertEqual(body["state"], "UNCOMMITTED")
        self.assertIsNone(case["enrollment"])

    def test_refused_on_drift_from_commit(self):
        case = self._committed_case("w4prodrift")
        _write_intake(case, {"patient.diagnosis": "a drifted diagnosis"})
        status, body = _http("POST", "/api/case/w4prodrift/promote",
                             {"actor": ENROLLER, "legal_basis": LEGAL_BASES[1]})
        self.assertEqual(status, 409)
        self.assertEqual(body["state"], "CONFIRMING")
        self.assertEqual(body["pending"], ["patient.diagnosis"])
        self.assertIsNone(case["enrollment"])

    def test_promote_records_enrollment_and_one_audit_record(self):
        case = self._committed_case("w4prook")
        before_intake = copy.deepcopy(case["intake"])
        body = self._promote_ok("w4prook", "waiver-164.512")
        enr = body["enrollment"]
        self.assertEqual(enr["actor"], ENROLLER)
        self.assertEqual(enr["legal_basis"], "waiver-164.512")
        self.assertEqual(enr["from_hash"],
                         case["committed_profile"]["profile_hash"])
        self.assertTrue(enr["at"].endswith("Z"))
        self.assertEqual(body["mode"], "ENROLLMENT")
        self.assertEqual(case["mode"], "ENROLLMENT")
        recs = [r for r in case["audit"] if r["action"] == "promote"]
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["actor"], ENROLLER)
        self.assertEqual(recs[0]["target"], "enrollment")
        self.assertEqual(recs[0]["input_hash"],
                         case["committed_profile"]["profile_hash"])
        self.assertEqual(recs[0]["detail"]["legal_basis"], "waiver-164.512")
        self.assertEqual(recs[0]["detail"]["from_mode"], "PREPARATORY_REVIEW")
        self.assertEqual(recs[0]["detail"]["to_mode"], "ENROLLMENT")
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])
        self.assertEqual(case["intake"], before_intake)   # intake untouched
        # GET /api/case exposes the enrollment block + live obligations.
        status, got = _http("GET", "/api/case/w4prook")
        self.assertEqual(status, 200)
        self.assertEqual(got["enrollment"], enr)
        self.assertEqual(got["mode"], "ENROLLMENT")
        self.assertEqual(len(got["obligations"]), 5)   # incl. 56.104(c) IRB notice

    def test_obligations_checklist_citations_and_hc3_honesty(self):
        # Sample fixture: non-emergency, fda_receipt_date = 2026-06-15.
        case = self._committed_case("w4proclocks")
        body = self._promote_ok("w4proclocks")
        checklist = body["obligations_checklist"]
        by_citation = {o["citation"]: o for o in checklist}
        self.assertEqual(sorted(by_citation), sorted([
            "21 CFR 312.32(c)(1)", "21 CFR 312.32(c)(2)",
            "21 CFR 312.310(d)(2)", "21 CFR 56.104(c)", "21 CFR 312.33"]))
        for o in checklist:
            self.assertEqual(o["owner"], "physician-sponsor")
            self.assertTrue(o["obligation"])
            if o["armed"]:
                self.assertRegex(o["due"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertIsNone(o["resolving_question"])
            else:   # HC3: unarmed = no date at all + the resolving question
                self.assertIsNone(o["due"])
                self.assertTrue(o["resolving_question"])
        # Safety-report clocks are per-event: ALWAYS unarmed at enrollment.
        self.assertFalse(by_citation["21 CFR 312.32(c)(1)"]["armed"])
        self.assertEqual(by_citation["21 CFR 312.32(c)(1)"]["days"], 15)
        self.assertFalse(by_citation["21 CFR 312.32(c)(2)"]["armed"])
        self.assertEqual(by_citation["21 CFR 312.32(c)(2)"]["days"], 7)
        # Non-emergency case, no phone authorization: both emergency-path
        # duties are listed but unarmed (MAJOR-1: 56.104(c) must be present).
        self.assertFalse(by_citation["21 CFR 312.310(d)(2)"]["armed"])
        self.assertFalse(by_citation["21 CFR 56.104(c)"]["armed"])
        # Annual report ARMS from the recorded receipt date via the canonical
        # clocks: effective 2026-07-15 (receipt+30, 312.40(b)(1)); first
        # anniversary 2027-07-15; due 60 calendar days later.
        annual = by_citation["21 CFR 312.33"]
        self.assertTrue(annual["armed"])
        self.assertEqual(annual["due"], "2027-09-13")
        self.assertEqual(annual["trigger_field"], "submission.fda_receipt_date")

    def test_emergency_followup_arms_from_recorded_authorization(self):
        case = self._committed_case("w4proemerg", extra={
            "submission.emergency": "true",
            # Fri 2026-06-26 + 15 working days (Jul 3 observed holiday
            # skipped) -> Mon 2026-07-20.
            "submission.emergency_auth_datetime": "2026-06-26",
        })
        body = self._promote_ok("w4proemerg", "treatment-disclosure")
        by = {o["citation"]: o for o in body["obligations_checklist"]}
        followup = by["21 CFR 312.310(d)(2)"]
        self.assertTrue(followup["armed"])
        self.assertEqual(followup["basis"], "working-day")
        self.assertEqual(followup["days"], 15)
        self.assertEqual(followup["due"], "2026-07-20")
        # MAJOR-1: the 5-working-day IRB notification (56.104(c)) — the shortest
        # deadline the emergency authorization arms — must be present and armed.
        irb = by["21 CFR 56.104(c)"]
        self.assertTrue(irb["armed"])
        self.assertEqual(irb["basis"], "working-day")
        self.assertEqual(irb["days"], 5)
        self.assertEqual(irb["due"], "2026-07-06")   # 6/26 +5wd, Jul-3 holiday skipped

    def test_unreadable_anchor_is_unarmed_never_guessed(self):
        case = self._committed_case("w4probaddate", extra={
            "submission.fda_receipt_date": "sometime in June"})
        body = self._promote_ok("w4probaddate")
        annual = [o for o in body["obligations_checklist"]
                  if o["citation"] == "21 CFR 312.33"][0]
        self.assertFalse(annual["armed"])
        self.assertIsNone(annual["due"])
        self.assertIn("could not be read", annual["resolving_question"])

    def test_repeat_promote_refused_record_stands(self):
        case = self._committed_case("w4prorepeat")
        self._promote_ok("w4prorepeat")
        first = copy.deepcopy(case["enrollment"])
        status, body = _http("POST", "/api/case/w4prorepeat/promote",
                             {"actor": "Someone Else, MD",
                              "legal_basis": LEGAL_BASES[2]})
        self.assertEqual(status, 409)
        self.assertIn("already enrolled", body["error"])
        self.assertEqual(body["enrollment"], first)      # the record stands
        self.assertEqual(case["enrollment"], first)      # nothing rewritten
        self.assertEqual(
            len([r for r in case["audit"] if r["action"] == "promote"]), 1)
        self.assertEqual(audit_mod.verify_chain(case["audit"]), [])

    def test_unknown_case_404(self):
        status, _ = _http("POST", "/api/case/nosuchcase77/promote",
                          {"actor": ENROLLER, "legal_basis": LEGAL_BASES[0]})
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# Micro-CRO board — read-only, reflects state, no action affordance
# ---------------------------------------------------------------------------

class TestCroBoard(Wave4TestBase):

    def _board_items(self):
        status, body = _http("GET", "/api/cro/board")
        self.assertEqual(status, 200)
        self.assertEqual(body["count"], len(body["board"]))
        self.assertIn("READ-ONLY", body["note"])
        return {item["case_id"]: item for item in body["board"]
                if item["case_id"] in self._case_ids}

    def test_board_has_no_post_route(self):
        status, _ = _http("POST", "/api/cro/board", {"anything": "at all"})
        self.assertEqual(status, 404)   # no acting affordance exists

    def test_board_reflects_case_state(self):
        self._register("w4boarddraft", self._sample_case())
        enrolled = self._committed_case("w4boardfull")
        server._generate_payload(enrolled)
        status, _ = _http("POST", "/api/case/w4boardfull/release",
                          {"actor": LINKER, "to": "manufacturer"})
        self.assertEqual(status, 200)
        self._promote_ok("w4boardfull")
        _http("POST", "/api/case/w4boardfull/patient-link", {"actor": LINKER})

        items = self._board_items()
        draft = items["w4boarddraft"]
        self.assertEqual(draft["stage"], "draft")
        self.assertEqual(draft["profile_state"], "UNCOMMITTED")
        self.assertEqual(draft["mode"], "PREPARATORY_REVIEW")
        self.assertFalse(draft["released"])
        self.assertFalse(draft["enrolled"])
        self.assertFalse(draft["patient_link_minted"])
        self.assertEqual(draft["obligations"], {"total": 0, "armed": 0})
        self.assertEqual(draft["patient_coded_id"], "PT-3926-014")
        self.assertEqual(draft["route_id"], "route-3926")
        self.assertEqual(draft["gates"]["required"], 4)
        self.assertEqual(draft["gates"]["signed"], 0)
        self.assertIsNone(draft["rollup_error"])
        self.assertGreater(sum(draft["ledger"].values()), 0)   # real rollup
        self.assertEqual(draft["clocks"]["total"], 1)          # non-emergency
        self.assertEqual(draft["clocks"]["armed"], 1)          # receipt date set

        full = items["w4boardfull"]
        self.assertEqual(full["stage"], "enrolled")
        self.assertEqual(full["profile_state"], "COMMITTED")
        self.assertEqual(full["mode"], "ENROLLMENT")
        self.assertTrue(full["released"])
        self.assertTrue(full["enrolled"])
        self.assertTrue(full["patient_link_minted"])
        self.assertEqual(full["obligations"]["total"], 5)   # incl. 56.104(c)
        self.assertEqual(full["obligations"]["armed"], 1)      # annual only

    def test_board_never_mutates_cases(self):
        case_a = self._register("w4boardnomut1", self._sample_case())
        case_b = self._committed_case("w4boardnomut2")
        before_a = copy.deepcopy(case_a)
        before_b = copy.deepcopy(case_b)
        _http("GET", "/api/cro/board")
        self.assertEqual(case_a, before_a)
        self.assertEqual(case_b, before_b)

    def test_board_survives_an_unrenderable_case(self):
        # A case whose data cannot render must appear with an honest rollup
        # error, not vanish from its own coordinator's view (and not 500).
        case = self._register("w4boardbroken", self._sample_case(extra={
            "submission.fda_receipt_date": "not-a-date"}))
        items = self._board_items()
        broken = items["w4boardbroken"]
        self.assertEqual(broken["rollup_error"], "TriggerDateError")
        self.assertIsNone(broken["ledger"])
        self.assertEqual(broken["stage"], "draft")   # stage still reported


class TestWave4ReviewPatches(Wave4TestBase):

    def test_board_carries_no_token_or_clinical_phi(self):
        # MINOR-6: the coordinator board is a coded summary — it must not carry
        # a patient_token (a capability) or clinical PHI (diagnosis/age/sex).
        case = self._committed_case("w4boardphi")
        _, mint = _http("POST", "/api/case/w4boardphi/patient-link",
                        {"actor": LINKER})   # mint a token to grep for
        token = mint["patient_token"]
        status, body = _http("GET", "/api/cro/board")
        self.assertEqual(status, 200)
        blob = json.dumps(body)
        self.assertNotIn(token, blob)
        self.assertNotIn("cholangiocarcinoma", blob.lower())
        for s in ("patient_token", "patient.diagnosis", "patient.age"):
            self.assertNotIn(s, blob)

    def test_non_string_actor_rejected_and_not_recorded(self):
        # MINOR-1: a dict/list actor must never be str()-baked into the
        # append-only record; it is rejected as a missing name.
        case = self._committed_case("w4actorobj")
        server._generate_payload(case)
        status, _ = _http("POST", "/api/case/w4actorobj/promote",
                          {"actor": {"name": "hax"},
                           "legal_basis": "authorization-164.508"})
        self.assertEqual(status, 400)
        self.assertIsNone(case.get("enrollment"))
        self.assertFalse([r for r in case.get("audit", [])
                          if r.get("action") == "promote"])


if __name__ == "__main__":
    unittest.main()
