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
        self.assertIs(ea_generators.written_3926_deadline,
                      clocks.written_3926_deadline)
        self.assertIs(ea_generators.irb_emergency_notification_deadline,
                      clocks.irb_emergency_notification_deadline)
        self.assertIs(ea_generators.ind_30_day_deadline, clocks.ind_30_day_deadline)
        self.assertIs(ea_generators.ind_annual_report_deadline,
                      clocks.ind_annual_report_deadline)
        # P1 split: the combined dual-anchor function is gone everywhere.
        self.assertFalse(hasattr(clocks, "expanded_access_emergency_deadlines"))
        self.assertFalse(hasattr(ea_generators, "expanded_access_emergency_deadlines"))
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


class ComputeClocksCanonicalTests(unittest.TestCase):
    """The route-declared clocks must agree, date for date, with the canonical
    named constructors in ossicro.clocks — proving the registry constants
    (15/5 working days, 30 calendar days) and the engine are one truth."""

    def _clocks_for(self, emergency, fields, as_of=None):
        route = routes.route_for_emergency(emergency)
        study = build_study(dict(fields), route)
        return ea_generators.compute_clocks(study, route, as_of=as_of), route

    def test_unanchored_clocks_are_unarmed_never_fabricated(self):
        # HC3: no trigger date entered -> armed False, null deadline, a
        # resolving question naming the trigger field — never a guessed date.
        for emergency in (True, False):
            out, route = self._clocks_for(emergency, {})
            self.assertEqual(len(out), len(route["clocks"]))
            for c in out:
                self.assertFalse(c["armed"], c["id"])
                self.assertIsNone(c["deadline"], c["id"])
                self.assertIsNone(c["days_remaining"], c["id"])
                self.assertIn(c["trigger_field"], c["resolving_question"], c["id"])

    def test_emergency_route_clocks_match_canonical_constructors(self):
        # Both emergency clocks anchored to Wed 2026-07-01 (observed July-3
        # holiday + weekends in range) must equal the canonical pair.
        out, _ = self._clocks_for(True, {
            "submission.emergency_auth_datetime": "2026-07-01",
            "submission.first_treatment_date": "2026-07-01",
        })
        by_id = {c["id"]: c for c in out}
        written = clocks.written_3926_deadline(authorization_date=D(2026, 7, 1))
        irb = clocks.irb_emergency_notification_deadline(first_treatment_date=D(2026, 7, 1))
        self.assertEqual(by_id["written-3926-15-working-day"]["deadline"],
                         written.due.isoformat())
        self.assertEqual(by_id["irb-notify-5-working-day"]["deadline"],
                         irb.due.isoformat())

    def test_nonemergency_route_clock_matches_ind_30_day_deadline(self):
        out, _ = self._clocks_for(False, {"submission.fda_receipt_date": "2026-06-15"})
        by_id = {c["id"]: c for c in out}
        canonical = clocks.ind_30_day_deadline(D(2026, 6, 15))
        self.assertEqual(by_id["ind-effective-30-day"]["deadline"],
                         canonical.due.isoformat())
        self.assertTrue(by_id["ind-effective-30-day"]["armed"])

    def test_days_remaining_matches_canonical_deadline_arithmetic(self):
        # Working-day clocks count working days; calendar clocks plain days —
        # exactly as clocks.Deadline.days_remaining computes them.
        as_of = D(2026, 7, 6)
        out, _ = self._clocks_for(True, {
            "submission.emergency_auth_datetime": "2026-07-01",
            "submission.first_treatment_date": "2026-07-01",
        }, as_of=as_of)
        by_id = {c["id"]: c for c in out}
        written = clocks.written_3926_deadline(authorization_date=D(2026, 7, 1))
        irb = clocks.irb_emergency_notification_deadline(first_treatment_date=D(2026, 7, 1))
        self.assertEqual(by_id["written-3926-15-working-day"]["days_remaining"],
                         written.days_remaining(as_of))
        self.assertEqual(by_id["irb-notify-5-working-day"]["days_remaining"],
                         irb.days_remaining(as_of))
        out, _ = self._clocks_for(False, {"submission.fda_receipt_date": "2026-06-15"},
                                  as_of=as_of)
        canonical = clocks.ind_30_day_deadline(D(2026, 6, 15))
        self.assertEqual(out[0]["days_remaining"], canonical.days_remaining(as_of))

    def test_garbled_trigger_raises_never_silently_unarmed(self):
        # HC2: a present-but-unparseable date is an error to surface, not an
        # absence to swallow (which would silently disarm a statutory clock).
        with self.assertRaises(ea_generators.TriggerDateError):
            self._clocks_for(True, {"submission.emergency_auth_datetime": "July 1, 2026"})

    def test_cover_letter_emergency_clock_carries_canonical_date(self):
        # The rendered cover letter's clock statement must state the canonical
        # 15-working-day deadline (21 CFR 312.310(d)(2)), not a recomputation.
        route = routes.route_for_emergency(True)
        study = build_study({
            "submission.emergency": "true",
            "submission.emergency_auth_datetime": "2026-07-01",
        }, route)
        doc = ea_generators.gen_cover_letter(study, load_documents())
        written = clocks.written_3926_deadline(authorization_date=D(2026, 7, 1))
        self.assertIn(written.due.isoformat(), doc.rendered)


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


class RendererHygieneTests(unittest.TestCase):
    """UI-QA F1/F2: no duplicated credential, no mid-sentence diagnosis seam."""

    def _render(self, gen, fields):
        route = routes.route_for_emergency(False)
        study = build_study(dict(fields), route)
        return getattr(ea_generators, gen)(study, load_documents(), as_of=D(2026, 7, 10)).rendered

    def test_no_duplicated_degree_when_name_carries_credential(self):
        # investigator.name from Practitioner.name already ends ", MD" and
        # investigator.degrees is a separate "MD" -> must not render "MD, MD".
        fields = dict(_load_sample_fields())
        fields["investigator.name"] = "Jordan A. Rivera, MD"
        fields["investigator.degrees"] = "MD"
        for gen in ("gen_cover_letter", "gen_loa_request", "gen_form_3926"):
            r = self._render(gen, fields)
            self.assertNotIn("MD, MD", r, gen)
            self.assertNotIn("[[MISSING: degrees_suffix]]", r, gen)

    def test_separate_degree_is_appended_when_absent_from_name(self):
        fields = dict(_load_sample_fields())
        fields["investigator.name"] = "Alex Kim"
        fields["investigator.degrees"] = "DO"
        r = self._render("gen_cover_letter", fields)
        self.assertIn("Alex Kim, DO", r)
        self.assertNotIn("[[MISSING: degrees_suffix]]", r)

    def test_diagnosis_not_spliced_mid_sentence(self):
        # The diagnosis narrative ends in a period; it must sit at sentence-end
        # ("Diagnosis: ...."), never mid-clause producing "...1., a serious".
        fields = dict(_load_sample_fields())
        for gen in ("gen_cover_letter", "gen_loa_request"):
            r = self._render(gen, fields)
            self.assertIn("Diagnosis:", r, gen)
            self.assertNotIn("., a serious", r, gen)
            self.assertNotIn(". — for which", r, gen)


if __name__ == "__main__":
    unittest.main(verbosity=2)
