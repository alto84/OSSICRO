"""Clock-engine tests. Run: `cd engine && python -m unittest tests.test_clocks -v`.

Verified against a fixed date table spanning weekends and federal holidays; no
reliance on the current date, so the arithmetic is reproducible (HC3)."""

import datetime
import unittest

from ossicro import clocks

D = datetime.date


class HolidayTests(unittest.TestCase):
    def test_2026_fixed_and_floating_holidays(self):
        h = clocks.federal_holidays(2026)
        self.assertEqual(h[D(2026, 1, 19)], "Birthday of Martin Luther King, Jr.")   # 3rd Mon Jan
        self.assertEqual(h[D(2026, 2, 16)], "Washington's Birthday")                 # 3rd Mon Feb
        self.assertEqual(h[D(2026, 5, 25)], "Memorial Day")                          # last Mon May
        self.assertEqual(h[D(2026, 9, 7)], "Labor Day")                              # 1st Mon Sep
        self.assertEqual(h[D(2026, 11, 26)], "Thanksgiving Day")                     # 4th Thu Nov

    def test_weekend_observance(self):
        # July 4, 2026 is a Saturday -> observed Friday July 3
        self.assertTrue(clocks.is_federal_holiday(D(2026, 7, 3)))
        self.assertFalse(clocks.is_working_day(D(2026, 7, 3)))
        self.assertFalse(clocks.is_federal_holiday(D(2026, 7, 4)))  # the actual Saturday is not the observed day


class WorkingDayTests(unittest.TestCase):
    def test_add_working_days_simple(self):
        # Fri 2026-07-31 + 5 working days -> Fri 2026-08-07 (no holidays in range)
        self.assertEqual(clocks.add_working_days(D(2026, 7, 31), 5), D(2026, 8, 7))

    def test_add_working_days_across_holiday(self):
        # Mon 2026-11-23 + 5 working days, Thanksgiving Thu 11-26 skipped -> Tue 2026-12-01
        self.assertEqual(clocks.add_working_days(D(2026, 11, 23), 5), D(2026, 12, 1))

    def test_add_working_days_rejects_nonpositive(self):
        with self.assertRaises(ValueError):
            clocks.add_working_days(D(2026, 1, 1), 0)


class DeadlineTests(unittest.TestCase):
    def test_written_3926_deadline_anchors_on_authorization(self):
        auth = D(2026, 7, 1)  # Wednesday
        w15 = clocks.written_3926_deadline(authorization_date=auth)
        self.assertEqual(w15.due, clocks.add_working_days(auth, 15))
        self.assertEqual(w15.citation, "21 CFR 312.310(d)(2)")
        self.assertEqual(w15.basis, "working-day")
        self.assertEqual(w15.anchor, auth)
        # July 3 (observed Independence Day) and both weekends fall inside the 15-working-day window
        self.assertGreater((w15.due - auth).days, 15)  # calendar span exceeds 15 due to skips

    def test_irb_emergency_notification_anchors_on_first_treatment(self):
        # M1: the 56.104(c) clock runs from the emergency USE (first
        # treatment), never from the FDA authorization date.
        ftd = D(2026, 7, 6)  # Monday
        w5 = clocks.irb_emergency_notification_deadline(first_treatment_date=ftd)
        self.assertEqual(w5.due, clocks.add_working_days(ftd, 5))
        self.assertEqual(w5.citation, "21 CFR 56.104(c)")
        self.assertEqual(w5.basis, "working-day")
        self.assertEqual(w5.anchor, ftd)

    def test_split_deadlines_refuse_the_other_anchor_semantics(self):
        # The split (Overhaul P1/M1) makes a swapped anchor a TypeError, not a
        # silent wrong date: each function accepts ONLY its own keyword-named
        # statutory anchor, and the combined dual-clock function is gone.
        d = D(2026, 7, 1)
        with self.assertRaises(TypeError):
            clocks.written_3926_deadline(d)                          # unnamed anchor
        with self.assertRaises(TypeError):
            clocks.written_3926_deadline(first_treatment_date=d)     # wrong event
        with self.assertRaises(TypeError):
            clocks.irb_emergency_notification_deadline(d)            # unnamed anchor
        with self.assertRaises(TypeError):
            clocks.irb_emergency_notification_deadline(authorization_date=d)  # wrong event
        self.assertFalse(hasattr(clocks, "expanded_access_emergency_deadlines"))

    def test_ind_30_day_is_calendar(self):
        d = clocks.ind_30_day_deadline(D(2026, 3, 1))
        self.assertEqual(d.due, D(2026, 3, 31))
        self.assertEqual(d.basis, "calendar-day")

    def test_ind_annual_report_deadline(self):
        # m16: receipt 2026-06-15 -> effective 2026-07-15 (312.40(b)(1)) ->
        # anniversary 2027-07-15 -> due 60 calendar days later, 2027-09-13.
        dl = clocks.ind_annual_report_deadline(D(2026, 6, 15))
        self.assertEqual(dl.due, D(2027, 9, 13))
        self.assertEqual(dl.citation, "21 CFR 312.33")
        self.assertEqual(dl.basis, "calendar-day")
        self.assertEqual(dl.anchor, D(2027, 7, 15))     # the anniversary
        self.assertEqual(dl.due, dl.anchor + datetime.timedelta(days=dl.n))

    def test_ind_annual_report_feb29_effective_date(self):
        # Leap-day effective date: receipt 2028-01-30 -> effective 2028-02-29;
        # anniversary Feb 28, 2029 (no Feb 29); due 60 days later, 2029-04-29.
        self.assertEqual(clocks.ind_30_day_deadline(D(2028, 1, 30)).due,
                         D(2028, 2, 29))
        dl = clocks.ind_annual_report_deadline(D(2028, 1, 30))
        self.assertEqual(dl.anchor, D(2029, 2, 28))
        self.assertEqual(dl.due, D(2029, 4, 29))


if __name__ == "__main__":
    unittest.main(verbosity=2)
