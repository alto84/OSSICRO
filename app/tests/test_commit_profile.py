"""INV-3 app-level tests: the commit-profile hard gate on the server payloads.

Design spec: docs/ehr-integration/commit-profile-design.md §8 items 9-16.
Drives the payload builders / endpoint core functions DIRECTLY with in-memory
case dicts and a tmp-patched CASES_DIR — no socket is ever bound (the live
UI-QA server on 8765 is never touched).
"""

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

from ossicro.profile import ProfileNotCommitted, profile_hash  # noqa: E402
from ossicro.review_port import DeterministicStubReviewer      # noqa: E402

ACTOR = "Jordan A. Rivera, MD"


def _write_intake(case, fields):
    """Mirror POST /intake's store rule: blanks stay honestly absent; any
    effective change bumps intake_rev."""
    before = dict(case["intake"])
    for key, value in fields.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            case["intake"].pop(key, None)
        else:
            case["intake"][key] = value
    if case["intake"] != before:
        case["intake_rev"] += 1


class ProfileTestBase(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="ossicro-test-cases-")
        self._orig_cases_dir = server.CASES_DIR
        server.CASES_DIR = self._tmp
        # Force the offline deterministic reviewer regardless of environment
        # (a live ANTHROPIC_API_KEY must never make a unit test egress).
        self._orig_select = server._select_reviewer
        server._select_reviewer = lambda: DeterministicStubReviewer()

    def tearDown(self):
        server.CASES_DIR = self._orig_cases_dir
        server._select_reviewer = self._orig_select
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _sample_case(self):
        case = server._new_case()
        _write_intake(case, server._sample_payload()["fields"])
        return case


# ---------------------------------------------------------------------------
# §8 item 9 — THE INV-3 NAMED TEST (privacy-state-machine.md §4 row INV-3):
# commit -> generate OK; mutate one confirmed field -> generate refused (the
# refusal names exactly that field) until re-confirmation; after confirm the
# new committed hash differs and generate succeeds, stamping the new hash.
# ---------------------------------------------------------------------------

class TestInv3CommitGate(ProfileTestBase):

    def test_inv3_commit_then_mutate_then_reconfirm(self):
        case = self._sample_case()

        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 200)
        self.assertEqual(body["profile"]["state"], "COMMITTED")
        old_hash = body["profile"]["profile_hash"]

        payload = server._generate_payload(case)
        self.assertTrue(payload["documents"])
        self.assertEqual(case["generated_hash"], old_hash)

        # Mutate ONE confirmed field -> refused, naming exactly that field.
        _write_intake(case, {"patient.diagnosis": "a different diagnosis"})
        with self.assertRaises(ProfileNotCommitted) as ctx:
            server._generate_payload(case)
        self.assertEqual(ctx.exception.state, "CONFIRMING")
        self.assertEqual(ctx.exception.pending, ["patient.diagnosis"])

        # Named re-confirmation -> recommit with a NEW hash.
        body, status = server._profile_confirm(
            case, {"actor": ACTOR, "field_ids": ["patient.diagnosis"]})
        self.assertEqual(status, 200)
        self.assertEqual(body["profile"]["state"], "COMMITTED")
        new_hash = body["profile"]["profile_hash"]
        self.assertNotEqual(new_hash, old_hash)

        payload = server._generate_payload(case)
        self.assertTrue(payload["documents"])
        self.assertEqual(case["generated_hash"], new_hash)  # new hash stamped
        # ...and the superseded commit is in history.
        history = case["committed_profile"]["history"]
        self.assertEqual(history[-1]["profile_hash"], old_hash)
        self.assertEqual(history[-1]["reconfirmed_fields"], ["patient.diagnosis"])


# ---------------------------------------------------------------------------
# §8 item 10 — generate/package refused on UNCOMMITTED (fail closed)
# ---------------------------------------------------------------------------

class TestUncommittedRefusal(ProfileTestBase):

    def test_generate_refused_uncommitted(self):
        case = self._sample_case()
        with self.assertRaises(ProfileNotCommitted) as ctx:
            server._generate_payload(case)
        self.assertEqual(ctx.exception.state, "UNCOMMITTED")
        self.assertIsNone(case["generated_hash"])   # nothing generated

    def test_package_refused_uncommitted(self):
        case = self._sample_case()
        with self.assertRaises(ProfileNotCommitted) as ctx:
            server._package_payload(case)
        self.assertEqual(ctx.exception.state, "UNCOMMITTED")

    def test_package_refused_on_drift(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.dose": "999 mg"})
        with self.assertRaises(ProfileNotCommitted) as ctx:
            server._package_payload(case)
        self.assertEqual(ctx.exception.state, "CONFIRMING")
        self.assertEqual(ctx.exception.pending, ["drug.dose"])


# ---------------------------------------------------------------------------
# §8 item 11 — /check runs in every state, stamps the TRUE consumed hash,
# injects the app-level resolving question, and never touches engine statuses
# ---------------------------------------------------------------------------

class TestCheckAllStates(ProfileTestBase):

    def _check_with_captured_stamp(self, case):
        captured = []
        orig = server.stamp_input_hash

        def capture(documents, input_hash):
            captured.append(input_hash)
            return orig(documents, input_hash)

        server.stamp_input_hash = capture
        try:
            payload = server._check_payload(case)
        finally:
            server.stamp_input_hash = orig
        return payload, captured

    def test_check_uncommitted_injects_question_and_stamps_true_hash(self):
        case = self._sample_case()
        payload, captured = self._check_with_captured_stamp(case)
        self.assertEqual(payload["profile"]["state"], "UNCOMMITTED")
        self.assertEqual(captured, [profile_hash(case["intake"])])
        injected = payload["ledger"][0]
        self.assertEqual(injected["doc_id"], "committed-profile")
        self.assertEqual(injected["status"], "red")
        self.assertIn("commit", injected["questions"][0]["text"].lower())

    def test_check_confirming_lists_pending_and_preserves_engine_statuses(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        committed_payload = server._check_payload(case)
        committed_statuses = {i["doc_id"]: i["status"]
                              for i in committed_payload["ledger"]}
        self.assertNotIn("committed-profile", committed_statuses)  # no injection

        _write_intake(case, {"patient.prior_therapies":
                             "gemcitabine/cisplatin then FOLFOX; progressed"})
        payload, captured = self._check_with_captured_stamp(case)
        self.assertEqual(payload["profile"]["state"], "CONFIRMING")
        self.assertEqual(payload["profile"]["pending"], ["patient.prior_therapies"])
        # true CONSUMED hash (drifted), not the committed hash
        self.assertEqual(captured, [profile_hash(case["intake"])])
        self.assertNotEqual(captured[0],
                            case["committed_profile"]["profile_hash"])
        injected = payload["ledger"][0]
        self.assertEqual(injected["doc_id"], "committed-profile")
        self.assertIn("patient.prior_therapies", injected["questions"][0]["text"])
        # engine ledger statuses otherwise unchanged (escalate-only preserved)
        drifted_statuses = {i["doc_id"]: i["status"] for i in payload["ledger"]
                            if i["doc_id"] != "committed-profile"}
        self.assertEqual(drifted_statuses, committed_statuses)

    def test_check_committed_no_injection_and_stamps_committed_hash(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        payload, captured = self._check_with_captured_stamp(case)
        self.assertEqual(payload["profile"]["state"], "COMMITTED")
        self.assertNotIn("committed-profile",
                         [i["doc_id"] for i in payload["ledger"]])
        # in COMMITTED the true consumed hash IS the committed hash
        self.assertEqual(captured, [case["committed_profile"]["profile_hash"]])


# ---------------------------------------------------------------------------
# §8 item 12 — revert: hash authority over the rev counter
# ---------------------------------------------------------------------------

class TestRevertHashAuthority(ProfileTestBase):

    def test_edit_then_revert_generates_with_original_hash(self):
        case = self._sample_case()
        original = case["intake"]["patient.diagnosis"]
        server._profile_commit(case, {"actor": ACTOR})
        committed_hash = case["committed_profile"]["profile_hash"]
        rev_at_commit = case["committed_profile"]["intake_rev_at_commit"]

        _write_intake(case, {"patient.diagnosis": "something else"})
        _write_intake(case, {"patient.diagnosis": original})   # reverted
        self.assertNotEqual(case["intake_rev"], rev_at_commit)  # counter moved

        # No re-confirmation demanded: the input equals what the named human
        # already confirmed. Generate succeeds with the ORIGINAL hash.
        payload = server._generate_payload(case)
        self.assertTrue(payload["documents"])
        self.assertEqual(case["generated_hash"], committed_hash)
        self.assertFalse(server._is_stale(case))


# ---------------------------------------------------------------------------
# §8 item 13 — migration: the literal 6-key legacy shape
# ---------------------------------------------------------------------------

class TestLegacyMigration(ProfileTestBase):

    LEGACY = {"generated_rev": 3, "intake": {"patient.coded_id": "ZZ-9",
                                             "drug.name": "legacydrug"},
              "intake_rev": 3, "route_id": "route-3926", "signoffs": []}

    def test_normalize_backfills_without_auto_commit(self):
        case = server._normalize_case(json.loads(json.dumps(self.LEGACY)))
        self.assertIsNone(case["committed_profile"])   # NO auto-commit, ever
        self.assertIsNone(case["generated_hash"])
        self.assertEqual(case["confirmations"], [])
        self.assertEqual(case["field_provenance"], {})

    def test_legacy_staleness_branch_byte_identical(self):
        # generated_rev == intake_rev -> not stale (today's rule, verbatim)
        case = server._normalize_case(json.loads(json.dumps(self.LEGACY)))
        self.assertFalse(server._is_stale(case))
        # intake mutates -> stale under the counter rule
        case["intake_rev"] = 4
        self.assertTrue(server._is_stale(case))
        # never generated -> never stale
        case2 = server._normalize_case(json.loads(json.dumps(self.LEGACY)))
        case2["generated_rev"] = None
        self.assertFalse(server._is_stale(case2))

    def test_legacy_generate_refused_never_committed(self):
        case = server._normalize_case(json.loads(json.dumps(self.LEGACY)))
        with self.assertRaises(ProfileNotCommitted) as ctx:
            server._generate_payload(case)
        self.assertEqual(ctx.exception.state, "UNCOMMITTED")
        self.assertIn("never committed", str(ctx.exception))


# ---------------------------------------------------------------------------
# §8 item 14 — attribution trail + INV-8 (hashes, never values)
# ---------------------------------------------------------------------------

class TestAttributionAndInv8(ProfileTestBase):

    DISTINCT = {"patient.coded_id": "ZQX-PATIENT-77",
                "patient.diagnosis": "XYZZY-DISTINCTIVE-DIAGNOSIS",
                "drug.name": "PLUGHVIB-999"}

    def test_commit_and_reconfirm_append_actioned_confirmations(self):
        case = server._new_case()
        _write_intake(case, dict(self.DISTINCT))
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.name": "PLUGHVIB-1000"})
        server._profile_confirm(case, {"actor": "Casey B. Ndiaye, RN",
                                       "field_ids": ["drug.name"]})
        actions = [(c.get("action"), c.get("actor"))
                   for c in case["confirmations"] if c.get("action")]
        self.assertEqual(actions, [("commit", ACTOR),
                                   ("reconfirm", "Casey B. Ndiaye, RN")])
        commit_rec = [c for c in case["confirmations"]
                      if c.get("action") == "commit"][0]
        self.assertEqual(commit_rec["field_ids"], sorted(self.DISTINCT))

    def test_committed_profile_contains_no_chart_values(self):
        case = server._new_case()
        _write_intake(case, dict(self.DISTINCT))
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.name": "PLUGHVIB-1000"})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["drug.name"]})
        blob = json.dumps(case["committed_profile"])
        for value in list(self.DISTINCT.values()) + ["PLUGHVIB-1000"]:
            self.assertNotIn(value, blob)   # INV-8: value hashes only


# ---------------------------------------------------------------------------
# §8 item 15 — §6.1 corollary: sign-off recorded against a superseded profile
# ---------------------------------------------------------------------------

class TestSignoffAdvisory(ProfileTestBase):

    GATE = "submission-to-fda"
    DOC = "form-fda-3926-individual-patient-expanded-access"

    def _signoff(self, case):
        record, err, status = server._record_signoff(case, {
            "gate_id": self.GATE, "doc_id": self.DOC,
            "signer_name": ACTOR, "role": "sponsor-investigator",
            "date": "2026-07-10"})
        self.assertIsNone(err)
        return record

    def _item(self, payload):
        return [i for i in payload["ledger"] if i["doc_id"] == self.DOC][0]

    def test_advisory_on_superseded_signoff_escalate_only(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        h1 = case["committed_profile"]["profile_hash"]
        record = self._signoff(case)
        self.assertEqual(record["input_hash"], h1)   # hash stamped at signoff

        before = self._item(server._check_payload(case))
        self.assertNotIn(server._PROFILE_ADVISORY, before["notes"])

        # field edited + re-confirmed -> H2; the H1 sign-off is superseded
        _write_intake(case, {"patient.prior_therapies": "updated narrative"})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["patient.prior_therapies"]})
        self.assertNotEqual(case["committed_profile"]["profile_hash"], h1)

        after = self._item(server._check_payload(case))
        self.assertIn(server._PROFILE_ADVISORY, after["notes"])
        # escalate-only: a note, never a demotion (or a promotion) — the gate
        # itself is neither cleared nor invalidated.
        self.assertEqual(after["status"], before["status"])

    def test_legacy_signoff_without_hash_is_exempt(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        record = self._signoff(case)
        record["input_hash"] = ""    # simulate a pre-INV-3 record on disk
        _write_intake(case, {"patient.prior_therapies": "updated narrative"})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["patient.prior_therapies"]})
        after = self._item(server._check_payload(case))
        self.assertNotIn(server._PROFILE_ADVISORY, after["notes"])


# ---------------------------------------------------------------------------
# §8 item 16 — FHIR composition: import maps only; applied proposals land in
# pending; named confirm; generate
# ---------------------------------------------------------------------------

class TestFhirComposition(ProfileTestBase):

    def test_import_apply_confirm_generate(self):
        case_id = "testfhircase1"
        case = server._new_case()
        server.CASES[case_id] = case
        try:
            _write_intake(case, server._sample_payload()["fields"])
            # Commit WITHOUT the two fields the proposals will add back.
            _write_intake(case, {"patient.age": "", "patient.sex": ""})
            server._profile_commit(case, {"actor": ACTOR})

            intake_before = dict(case["intake"])
            result, err, status = server._fhir_import(
                case, case_id, {"use_sample": True})
            self.assertIsNone(err)
            self.assertEqual(case["intake"], intake_before)   # maps only (INV-2)

            proposals = {p["field_id"]: p["value"] for p in result["proposals"]}
            subset = {fid: proposals[fid]
                      for fid in ("patient.age", "patient.sex")}
            _write_intake(case, subset)   # physician applies via /intake

            self.assertEqual(server._profile_block(case)["pending"],
                             ["patient.age", "patient.sex"])
            with self.assertRaises(ProfileNotCommitted):
                server._generate_payload(case)

            body, st = server._profile_confirm(
                case, {"actor": ACTOR,
                       "field_ids": ["patient.age", "patient.sex"]})
            self.assertEqual(st, 200)
            self.assertEqual(body["profile"]["state"], "COMMITTED")
            payload = server._generate_payload(case)
            self.assertTrue(payload["documents"])
        finally:
            server.CASES.pop(case_id, None)


# ---------------------------------------------------------------------------
# Endpoint-core validation shapes (design §5.3)
# ---------------------------------------------------------------------------

class TestEndpointValidation(ProfileTestBase):

    def test_commit_blank_actor_400(self):
        case = self._sample_case()
        body, status = server._profile_commit(case, {"actor": "   "})
        self.assertEqual(status, 400)
        self.assertIn("error", body)
        self.assertIsNone(case["committed_profile"])

    def test_commit_empty_intake_400(self):
        case = server._new_case()
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 400)
        self.assertIsNone(case["committed_profile"])

    def test_commit_with_pending_409_names_fields(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        _write_intake(case, {"drug.dose": "42 mg"})
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 409)
        self.assertEqual(body["pending"], ["drug.dose"])
        self.assertEqual(body["state"], "CONFIRMING")

    def test_confirm_non_pending_field_400(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        body, status = server._profile_confirm(
            case, {"actor": ACTOR, "field_ids": ["drug.name"]})
        self.assertEqual(status, 400)
        self.assertIn("not pending", body["error"])

    def test_confirm_before_any_commit_400(self):
        case = self._sample_case()
        body, status = server._profile_confirm(
            case, {"actor": ACTOR, "field_ids": ["drug.name"]})
        self.assertEqual(status, 400)

    def test_get_case_profile_block_shape(self):
        case = self._sample_case()
        block = server._profile_block(case)
        self.assertEqual(block, {"state": "UNCOMMITTED", "profile_hash": None,
                                 "pending": [], "committed_by": None,
                                 "committed_at": None})
        server._profile_commit(case, {"actor": ACTOR})
        block = server._profile_block(case)
        self.assertEqual(block["state"], "COMMITTED")
        self.assertEqual(block["committed_by"], ACTOR)
        self.assertTrue(block["profile_hash"].startswith("sha256:"))


# ---------------------------------------------------------------------------
# Review-round patches: B1 (snapshot under concurrent mutation), M1 (recommit-
# needed dead-end), m2 (idempotent-recommit history dedupe).
# ---------------------------------------------------------------------------

class TestReviewPatches(ProfileTestBase):

    def test_b1_package_uses_gated_snapshot_under_mutation(self):
        # B1: a racing POST /intake during the build must not change what the
        # gate approved. build_study must receive the pre-mutation snapshot.
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        real_build = server.build_study
        seen = {}

        def spy(intake, route):
            seen["intake"] = dict(intake)
            case["intake"]["drug.dose"] = "MUTATED-CONCURRENTLY"  # racing writer
            return real_build(intake, route)

        server.build_study = spy
        try:
            pkg = server._package_payload(case)          # must not raise
        finally:
            server.build_study = real_build
        # the build consumed the committed snapshot, not the concurrent mutation
        self.assertNotIn("MUTATED-CONCURRENTLY", json.dumps(seen["intake"]))
        self.assertTrue(pkg["documents"])

    def test_m1_recommit_needed_state_has_an_action(self):
        # commit {a,b,c} -> edit a,b -> confirm a (staged) -> revert b.
        # pending drains to [] but the hash still differs: state must be
        # CONFIRMING with recommit_needed True, and a plain commit must rescue.
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        dx0 = case["intake"]["patient.diagnosis"]
        pt0 = case["intake"]["patient.prior_therapies"]
        _write_intake(case, {"patient.diagnosis": "edited dx",
                             "patient.prior_therapies": "edited pt"})
        server._profile_confirm(case, {"actor": ACTOR,
                                       "field_ids": ["patient.diagnosis"]})
        _write_intake(case, {"patient.prior_therapies": pt0})   # revert b
        block = server._profile_block(case)
        self.assertEqual(block["state"], "CONFIRMING")
        self.assertEqual(block["pending"], [])
        self.assertTrue(block["recommit_needed"])
        # generation still fail-closed here...
        with self.assertRaises(ProfileNotCommitted):
            server._generate_payload(case)
        # ...and a plain recommit rescues (folds the staged diagnosis in).
        body, status = server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(status, 200)
        self.assertEqual(body["profile"]["state"], "COMMITTED")
        self.assertTrue(server._generate_payload(case)["documents"])

    def test_m2_idempotent_recommit_does_not_grow_history(self):
        case = self._sample_case()
        server._profile_commit(case, {"actor": ACTOR})
        h0 = len(case["committed_profile"]["history"])
        server._profile_commit(case, {"actor": ACTOR})   # nothing changed
        server._profile_commit(case, {"actor": ACTOR})
        self.assertEqual(len(case["committed_profile"]["history"]), h0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
