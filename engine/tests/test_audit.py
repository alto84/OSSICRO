"""I-AUDIT engine tests: the append-only audit log (BUILD-PLAN Wave 1).

Two load-bearing properties:

  APPEND-ONLY — the module's API offers no mutation or deletion of an
  existing record, appending never alters prior entries, and everything the
  API hands back (append's return, read's views) is frozen and detached
  from the stored trail.

  PHI-FREE (INV-8) — a trail written through the API for a realistic case
  flow contains field ids, actions, actors, timestamps, and hashes, and
  NEVER a chart value; structured detail payloads that could smuggle values
  are refused loudly.
"""

import dataclasses
import json
import pathlib
import re
import sys
import unittest

ENGINE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from ossicro import audit  # noqa: E402
from ossicro.profile import field_value_hash, profile_hash  # noqa: E402

ACTOR = "Jordan A. Rivera, MD"

# Distinctive synthetic chart values: they exist in the TEST's scope so the
# assertion "none of these ever appears in the trail" is meaningful.
CHART = {"patient.diagnosis": "XYZZY-DISTINCTIVE-DIAGNOSIS",
         "patient.coded_id": "ZQX-PATIENT-77",
         "drug.name": "PLUGHVIB-999"}


def _sample_flow_trail():
    """A trail written the way the app writes it: ids + hashes, no values."""
    trail = []
    audit.append(trail, actor=ACTOR, action="commit",
                 target="committed-profile",
                 input_hash=profile_hash(CHART),
                 detail={"field_ids": sorted(CHART)})
    audit.append(trail, actor="Casey B. Ndiaye, RN", action="reconfirm",
                 target="committed-profile",
                 input_hash=field_value_hash(CHART["drug.name"]),
                 detail={"field_ids": ["drug.name"]})
    audit.append(trail, actor=ACTOR, action="signoff",
                 target="form-fda-3926-individual-patient-expanded-access",
                 input_hash=profile_hash(CHART),
                 detail={"gate_id": "submission-to-fda", "role":
                         "sponsor-investigator", "date": "2026-07-10"})
    audit.append(trail, actor="", action="bundle_loaded",
                 target="fhir-bundle", input_hash="sha256:" + "0" * 64,
                 detail={"source_kind": "upload", "proposals": 7})
    return trail


class TestAppendOnly(unittest.TestCase):

    def test_seq_is_strictly_increasing_from_one(self):
        trail = _sample_flow_trail()
        self.assertEqual([r["seq"] for r in trail], [1, 2, 3, 4])
        self.assertEqual(audit.last_seq(trail), 4)
        self.assertEqual(audit.last_seq([]), 0)

    def test_append_never_alters_existing_records(self):
        trail = _sample_flow_trail()
        snapshot = json.dumps(trail, sort_keys=True)
        audit.append(trail, actor=ACTOR, action="egress_query",
                     target="clinicaltrials.gov")   # arbitrary future action
        self.assertEqual(json.dumps(trail[:4], sort_keys=True), snapshot)
        self.assertEqual(trail[4]["seq"], 5)

    def test_module_exposes_no_mutation_or_deletion_api(self):
        # The whole write surface is `append`; nothing removes or rewrites.
        # verify_chain is read-only (tamper detection), not a mutator.
        self.assertEqual(sorted(audit.__all__),
                         ["AuditRecord", "append", "last_seq", "read", "verify_chain"])
        for name in dir(audit):
            self.assertIsNone(
                re.match(r"(remove|delete|update|edit|pop|clear|rewrite)",
                         name, re.IGNORECASE),
                "audit module must not expose a mutator: %r" % name)

    def test_returned_records_are_frozen(self):
        trail = _sample_flow_trail()
        for rec in [audit.append(trail, actor=ACTOR, action="x")] + audit.read(trail):
            with self.assertRaises(dataclasses.FrozenInstanceError):
                rec.actor = "someone else"
            with self.assertRaises(TypeError):
                rec.detail["injected"] = "nope"     # mappingproxy

    def test_read_views_are_detached_copies(self):
        trail = _sample_flow_trail()
        before = json.dumps(trail, sort_keys=True)
        views = audit.read(trail)
        # list detail values come back as tuples — immutable, not aliases
        self.assertEqual(views[0].detail["field_ids"], tuple(sorted(CHART)))
        self.assertEqual(json.dumps(trail, sort_keys=True), before)

    def test_callers_later_mutation_of_detail_cannot_reach_the_trail(self):
        trail = []
        detail = {"field_ids": ["drug.name"]}
        audit.append(trail, actor=ACTOR, action="commit", detail=detail)
        detail["field_ids"].append("smuggled.after.the.fact")
        self.assertEqual(trail[0]["detail"]["field_ids"], ["drug.name"])

    def test_blank_action_refused(self):
        with self.assertRaises(ValueError):
            audit.append([], actor=ACTOR, action="   ")

    def test_trail_must_be_a_list(self):
        with self.assertRaises(ValueError):
            audit.append({"not": "a list"}, actor=ACTOR, action="commit")

    def test_arbitrary_action_strings_accepted(self):
        # INV-4 egress / INV-5 enrollment / release write to this same trail.
        trail = []
        for action in ("egress_query", "promote", "release"):
            rec = audit.append(trail, actor=ACTOR, action=action)
            self.assertEqual(rec.action, action)

    def test_records_are_json_serializable(self):
        trail = _sample_flow_trail()
        self.assertEqual(json.loads(json.dumps(trail)), trail)


class TestPhiFree(unittest.TestCase):

    def test_sample_flow_trail_contains_no_chart_values(self):
        blob = json.dumps(_sample_flow_trail())
        for value in CHART.values():
            self.assertNotIn(value, blob)   # INV-8: ids and hashes only

    def test_structured_detail_refused(self):
        # A nested object is exactly the shape a chart value would ride in.
        for bad in ({"observation": {"value": "142 mg/dL"}},
                    {"rows": [{"dx": "XYZZY"}]},
                    {b"bytes-key": "x"}):
            with self.assertRaises(ValueError):
                audit.append([], actor=ACTOR, action="commit", detail=bad)

    def test_record_carries_only_the_declared_keys(self):
        trail = _sample_flow_trail()
        for rec in trail:
            self.assertEqual(sorted(rec), ["action", "actor", "at", "detail",
                                           "input_hash", "prev_hash", "rec_hash",
                                           "seq", "target"])
            self.assertRegex(rec["at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class TestHashChain(unittest.TestCase):
    """MINOR-7: append-only is cryptographically checkable, not convention-only."""

    def test_intact_chain_verifies(self):
        trail = _sample_flow_trail()
        self.assertEqual(audit.verify_chain(trail), [])   # no breaks

    def test_each_record_binds_its_predecessor(self):
        trail = []
        audit.append(trail, actor=ACTOR, action="commit")
        audit.append(trail, actor=ACTOR, action="reconfirm")
        self.assertEqual(trail[0]["prev_hash"], "")
        self.assertEqual(trail[1]["prev_hash"], trail[0]["rec_hash"])
        self.assertTrue(trail[0]["rec_hash"].startswith("sha256:"))

    def test_tampered_record_is_detected(self):
        trail = _sample_flow_trail()
        # Silently rewrite history the way a direct file edit or an in-process
        # bug would — the chain must expose it.
        trail[0]["actor"] = "Someone Else"
        broken = audit.verify_chain(trail)
        self.assertIn(trail[0]["seq"], broken)

    def test_deleted_record_is_detected(self):
        trail = _sample_flow_trail()
        self.assertGreater(len(trail), 2)
        del trail[1]                       # drop a middle record
        self.assertTrue(audit.verify_chain(trail))   # chain now broken


if __name__ == "__main__":
    unittest.main(verbosity=2)
