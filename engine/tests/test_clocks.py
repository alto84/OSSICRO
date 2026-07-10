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
    def test_emergency_deadlines(self):
        auth = D(2026, 7, 1)  # Wednesday
        dls = {d.name: d for d in clocks.expanded_access_emergency_deadlines(auth)}
        w15 = dls["Written expanded-access submission to FDA"]
        w5 = dls["IRB notification of emergency use"]
        self.assertEqual(w15.due, clocks.add_working_days(auth, 15))
        self.assertEqual(w5.due, clocks.add_working_days(auth, 5))
        self.assertEqual(w15.citation, "21 CFR 312.310(d)(2)")
        # July 3 (observed Independence Day) and both weekends fall inside the 15-working-day window
        self.assertGreater((w15.due - auth).days, 15)  # calendar span exceeds 15 due to skips

    def test_ind_30_day_is_calendar(self):
        d = clocks.ind_30_day_deadline(D(2026, 3, 1))
        self.assertEqual(d.due, D(2026, 3, 31))
        self.assertEqual(d.basis, "calendar-day")


if __name__ == "__main__":
    unittest.main(verbosity=2)
