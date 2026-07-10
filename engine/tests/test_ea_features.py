"""Tests for the Route-3926 backend feature additions.

Covers three shared-contract guarantees:
- the synthetic sample intake loads and yields a mostly-green, submission-ready
  package (only the non-delegable human-gate ambers remain);
- the EA clock plumbing sources its arithmetic from the canonical
  ossicro.clocks engine (no duplicate calendar), matching a known date;
- every bundled package document hashes to its manifest sha256, i.e.
  sha256(rendered.utf8) is reproducible by a standalone verifier.

Run: `cd engine && python -m unittest tests.test_ea_features -v`.
"""

import datetime
import hashlib
import json
import unittest
from pathlib import Path

from ossicro import clocks, routes
from ossicro import ea_generators
from ossicro.assemble import assemble_submission
from ossicro.ea_generators import build_study, generate_route_documents
from ossicro.pipeline import run_check
from ossicro.registry import load_documents, load_gates

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

D = datetime.date


def _load_sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return data.get("fields", data)


def _assemble_sample():
    fields = _load_sample_fields()
    emergency = str(fields.get("submission.emergency", "")).strip().lower() in ("true", "1", "yes")
    route = routes.route_for_emergency(emergency)
    study = build_study(fields, route)
    documents = generate_route_documents(study, route, route_docreg := load_documents())
    return study, documents, route, route_docreg


class SampleCaseTests(unittest.TestCase):
    def test_sample_file_is_wellformed_intake(self):
        fields = _load_sample_fields()
        self.assertIsInstance(fields, dict)
        # every value is a non-empty string (a clean intake carries no blanks)
        for key, value in fields.items():
            self.assertIsInstance(value, str, key)
            self.assertTrue(value.strip(), key)
        # required intake fields (per the shared schema) are all supplied
        required = [f["id"] for f in routes.intake_fields() if f.get("required")]
        for field_id in required:
            self.assertIn(field_id, fields, "sample missing required field %s" % field_id)
        # no direct-identifier leakage: coded id only
        self.assertNotIn("patient.name", fields)

    def test_sample_yields_mostly_green_submission_ready(self):
        study, documents, route, docreg = _assemble_sample()
        gatereg = load_gates()
        result = run_check(study, documents, docreg, gatereg)
        statuses = [item.status for item in result.ledger]
        # zero reds: the only non-green items are the non-delegable human gates
        self.assertNotIn("red", statuses)
        self.assertIn("green", statuses)
        self.assertIn("amber", statuses)
        # every amber carries a gate id (a pending human act, not a doc gap)
        for item in result.ledger:
            if item.status == "amber":
                self.assertTrue(item.gate_id, item.doc_id)
        pkg = assemble_submission(study, documents, route, docreg, gatereg)
        self.assertTrue(pkg["submission_ready"])
        self.assertEqual(pkg["blocking"], [])

    def test_sample_never_clears_a_gate(self):
        # HARD LINE: a green/complete package still surfaces the human gates.
        study, documents, route, docreg = _assemble_sample()
        gatereg = load_gates()
        pkg = assemble_submission(study, documents, route, docreg, gatereg)
        result = run_check(study, documents, docreg, gatereg)
        gate_ids = {pg.gate_id for pg in result.gate_packet}
        self.assertIn("submission-to-fda", gate_ids)
        self.assertIn("informed-consent", gate_ids)


class ClockReconciliationTests(unittest.TestCase):
    def test_ea_clock_functions_come_from_clocks_module(self):
        # ea_generators must re-export the canonical engine, not shadow it.
        self.assertIs(ea_generators.add_working_days, clocks.add_working_days)
        self.assertIs(ea_generators.federal_holidays, clocks.federal_holidays)
        self.assertIs(ea_generators.expanded_access_emergency_deadlines,
                      clocks.expanded_access_emergency_deadlines)
        self.assertIs(ea_generators.ind_30_day_deadline, clocks.ind_30_day_deadline)
        # the duplicate inline calendar is gone
        self.assertFalse(hasattr(ea_generators, "us_federal_holidays"))

    def test_compute_deadline_matches_known_dates(self):
        # 15 working days after Wed 2026-07-01, skipping observed July-3 holiday
        # and two weekends, matches the canonical engine exactly.
        expected_working = clocks.add_working_days(D(2026, 7, 1), 15).isoformat()
        self.assertEqual(
            ea_generators.compute_deadline("2026-07-01", 15, "working"),
            expected_working,
        )
        # 30 calendar days after 2026-06-15 is 2026-07-15 (plain span).
        self.assertEqual(
            ea_generators.compute_deadline("2026-06-15", 30, "calendar"),
            "2026-07-15",
        )
        # no trigger -> honestly None (never guessed)
        self.assertIsNone(ea_generators.compute_deadline(None, 15, "working"))


class ManifestHashTests(unittest.TestCase):
    def test_manifest_sha256_equals_sha256_of_rendered(self):
        study, documents, route, docreg = _assemble_sample()
        gatereg = load_gates()
        pkg = assemble_submission(study, documents, route, docreg, gatereg)
        self.assertTrue(pkg["documents"])
        self.assertEqual(len(pkg["documents"]), len(pkg["manifest"]))
        rendered_by_doc = {d["doc_id"]: d["rendered"] for d in pkg["documents"]}
        for entry in pkg["manifest"]:
            rendered = rendered_by_doc[entry["doc_id"]]
            recomputed = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
            self.assertEqual(recomputed, entry["sha256"], entry["doc_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
