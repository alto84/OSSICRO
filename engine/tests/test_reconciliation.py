"""Overhaul P1 [PT-6] — cross-artifact statutory-clock reconciliation.

Given ONE intake fact set, every surface that states a deadline for the same
statutory duty must state the SAME date:

- the route registry's clock (routes.json, via ea_generators.compute_clocks),
- the generator's computed deadline paragraph (the rendered cover letter /
  IRB concurrence request),
- the app's sponsor-obligations checklist row
  (app/server.py:_sponsor_obligations),
- and the canonical single-anchor engine helper in ossicro.clocks.

Duties reconciled: 21 CFR 312.310(d)(2) from the FDA AUTHORIZATION date;
21 CFR 56.104(c) from the FIRST-TREATMENT date (M1: a different event);
21 CFR 312.33 (via 312.40(b)(1)) from the FDA receipt date. This test is the
tripwire M1 lacked — a re-unified anchor or a drifted copy of the arithmetic
fails here, date for date.

The app server module is imported (never started, never bound: import is
side-effect-free; the suite never touches :8765).

Run: `cd engine && python -m unittest tests.test_reconciliation -v`.
"""

import datetime
import json
import sys
import unittest
from pathlib import Path

from ossicro import clocks, ea_generators, routes
from ossicro.ea_generators import build_study, compute_clocks
from ossicro.registry import load_documents

ENGINE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ENGINE_ROOT.parent
APP_DIR = str(REPO_ROOT / "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import server  # noqa: E402  (the app backend; imported, never bound)

D = datetime.date
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

# ONE fact set, three recorded anchor dates — deliberately all different so a
# swapped anchor cannot hide behind equal dates.
AUTH_DATE = "2026-06-26"          # FDA telephone authorization (Friday)
FIRST_TREATMENT = "2026-07-06"    # emergency use / first treatment (Monday)
FDA_RECEIPT = "2026-06-15"        # FDA receipt of the written 3926


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _emergency_fields():
    fields = _sample_fields()
    fields.update({
        "submission.emergency": "true",
        "submission.emergency_auth_datetime": AUTH_DATE,
        "submission.first_treatment_date": FIRST_TREATMENT,
    })
    return fields


def _obligations(intake):
    """The app checklist for an enrolled case with this intake."""
    case = {
        "enrollment": {"actor": "Reconciliation Test, MD",
                       "at": "2026-07-10T00:00:00Z",
                       "legal_basis": "treatment-disclosure"},
        "intake": dict(intake),
    }
    return {o["citation"]: o for o in server._sponsor_obligations(case)}


class EmergencyClockReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.fields = _emergency_fields()
        self.route = routes.route_for_emergency(True)
        self.study = build_study(dict(self.fields), self.route)
        self.route_clocks = {c["id"]: c
                             for c in compute_clocks(self.study, self.route)}
        self.obligations = _obligations(self.fields)

    def test_written_3926_same_due_everywhere(self):
        canonical = clocks.written_3926_deadline(
            authorization_date=D(2026, 6, 26))
        due = canonical.due.isoformat()
        # route registry clock
        self.assertEqual(
            self.route_clocks["written-3926-15-working-day"]["deadline"], due)
        # generator paragraph (cover letter clock statement)
        cover = ea_generators.gen_cover_letter(self.study, load_documents())
        self.assertIn(due, cover.rendered)
        # app obligations row
        row = self.obligations["21 CFR 312.310(d)(2)"]
        self.assertTrue(row["armed"])
        self.assertEqual(row["due"], due)
        self.assertEqual(row["trigger_field"],
                         "submission.emergency_auth_datetime")

    def test_irb_notification_same_due_everywhere_from_first_treatment(self):
        canonical = clocks.irb_emergency_notification_deadline(
            first_treatment_date=D(2026, 7, 6))
        due = canonical.due.isoformat()
        # route registry clock
        self.assertEqual(
            self.route_clocks["irb-notify-5-working-day"]["deadline"], due)
        # generator paragraph (IRB request pathway statement)
        irb_req = ea_generators.gen_irb_request(self.study, load_documents())
        self.assertIn(due, irb_req.rendered)
        # app obligations row
        row = self.obligations["21 CFR 56.104(c)"]
        self.assertTrue(row["armed"])
        self.assertEqual(row["due"], due)
        self.assertEqual(row["trigger_field"],
                         "submission.first_treatment_date")

    def test_the_two_emergency_duties_do_not_share_an_anchor(self):
        # M1 regression pin: with different recorded anchor dates the two
        # deadlines MUST differ — equal dates would mean a re-unified anchor.
        w = self.obligations["21 CFR 312.310(d)(2)"]["due"]
        i = self.obligations["21 CFR 56.104(c)"]["due"]
        self.assertNotEqual(w, i)
        # and neither equals what the WRONG anchor would have produced
        wrong_irb = clocks.irb_emergency_notification_deadline(
            first_treatment_date=D(2026, 6, 26)).due.isoformat()
        self.assertNotEqual(i, wrong_irb)

    def test_irb_clock_unarmed_without_first_treatment_all_surfaces(self):
        fields = _emergency_fields()
        del fields["submission.first_treatment_date"]
        study = build_study(dict(fields), self.route)
        rc = {c["id"]: c for c in compute_clocks(study, self.route)}
        self.assertFalse(rc["irb-notify-5-working-day"]["armed"])
        self.assertIsNone(rc["irb-notify-5-working-day"]["deadline"])
        row = _obligations(fields)["21 CFR 56.104(c)"]
        self.assertFalse(row["armed"])
        self.assertIsNone(row["due"])
        self.assertTrue(row["resolving_question"])


class NonEmergencyClockReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.fields = _sample_fields()
        self.fields["submission.fda_receipt_date"] = FDA_RECEIPT
        self.route = routes.route_for_emergency(False)
        self.study = build_study(dict(self.fields), self.route)

    def test_ind_effective_30_day_same_due_everywhere(self):
        canonical = clocks.ind_30_day_deadline(D(2026, 6, 15))
        due = canonical.due.isoformat()
        rc = {c["id"]: c for c in compute_clocks(self.study, self.route)}
        self.assertEqual(rc["ind-effective-30-day"]["deadline"], due)
        cover = ea_generators.gen_cover_letter(self.study, load_documents())
        self.assertIn(due, cover.rendered)

    def test_annual_report_app_row_equals_engine_helper(self):
        # m16: the app row and the engine helper are the SAME arithmetic —
        # because the app now calls the helper instead of copying the math.
        canonical = clocks.ind_annual_report_deadline(D(2026, 6, 15))
        row = _obligations(self.fields)["21 CFR 312.33"]
        self.assertTrue(row["armed"])
        self.assertEqual(row["due"], canonical.due.isoformat())
        self.assertEqual(row["due"], "2027-09-13")   # fixed-table pin (HC3)

    def test_annual_report_feb29_case_via_app_row(self):
        # Feb-29 effective date, reconciled through the app surface too.
        fields = dict(self.fields)
        fields["submission.fda_receipt_date"] = "2028-01-30"
        row = _obligations(fields)["21 CFR 312.33"]
        canonical = clocks.ind_annual_report_deadline(D(2028, 1, 30))
        self.assertEqual(row["due"], canonical.due.isoformat())
        self.assertEqual(row["due"], "2029-04-29")


if __name__ == "__main__":
    unittest.main(verbosity=2)
