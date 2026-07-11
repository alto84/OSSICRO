"""Working-day clock engine (HC3: statutory clocks are computed, never judged).

Deterministic US federal-holiday + weekend arithmetic for the deadlines that
govern expanded access and IND conduct. Pure stdlib; operates on given anchor
dates (a recorded authorization date, an event date) — never on "now" — so its
output is reproducible and testable against a fixed table.

Federal holidays follow 5 U.S.C. 6103 with the OPM weekend-observance rule: a
fixed-date holiday on Saturday is observed the preceding Friday; on Sunday, the
following Monday. Monday-anchored holidays never fall on a weekend.

The clocks implemented (each cited where used):
- 15 WORKING DAYS — written submission of an individual-patient expanded-access
  request after emergency authorization (21 CFR 312.310(d)(2)).
- 5 WORKING DAYS — IRB notification after emergency use of the test article
  (21 CFR 56.104(c)); the clock runs from the emergency use (first treatment).
The 30-DAY IND wait (312.40(b)(1)) is a CALENDAR-day clock, also provided.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Dict, List

_DAY = datetime.timedelta(days=1)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime.date:
    """The nth (1-based) given weekday (Mon=0) of a month."""
    d = datetime.date(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + datetime.timedelta(days=offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> datetime.date:
    if month == 12:
        d = datetime.date(year, 12, 31)
    else:
        d = datetime.date(year, month + 1, 1) - _DAY
    return d - datetime.timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d: datetime.date) -> datetime.date:
    """Apply the weekend-observance rule to a fixed-date holiday."""
    if d.weekday() == 5:            # Saturday -> Friday
        return d - _DAY
    if d.weekday() == 6:            # Sunday -> Monday
        return d + _DAY
    return d


def federal_holidays(year: int) -> Dict[datetime.date, str]:
    """The observed US federal holidays falling within a calendar year.

    New Year's Day is the one holiday whose observance can cross a year
    boundary: when January 1 of year N+1 is a Saturday it is observed on
    December 31 of year N, so that observed date belongs to year N's table
    (and, symmetrically, a Saturday January 1 of THIS year is observed in the
    prior year and is excluded here). Every entry returned falls in ``year``.
    """
    h = {
        _observed(datetime.date(year, 1, 1)): "New Year's Day",
        _nth_weekday(year, 1, 0, 3): "Birthday of Martin Luther King, Jr.",
        _nth_weekday(year, 2, 0, 3): "Washington's Birthday",
        _last_weekday(year, 5, 0): "Memorial Day",
        _observed(datetime.date(year, 6, 19)): "Juneteenth National Independence Day",
        _observed(datetime.date(year, 7, 4)): "Independence Day",
        _nth_weekday(year, 9, 0, 1): "Labor Day",
        _nth_weekday(year, 10, 0, 2): "Columbus Day",
        _observed(datetime.date(year, 11, 11)): "Veterans Day",
        _nth_weekday(year, 11, 3, 4): "Thanksgiving Day",
        _observed(datetime.date(year, 12, 25)): "Christmas Day",
    }
    # Next year's New Year's Day, when observed on this year's Dec 31.
    next_nyd = _observed(datetime.date(year + 1, 1, 1))
    if next_nyd.year == year:
        h[next_nyd] = "New Year's Day"
    # Drop any observed date that fell outside this year (a Saturday Jan 1
    # observed the prior Dec 31 belongs to the prior year's table).
    return {d: name for d, name in h.items() if d.year == year}


def is_federal_holiday(d: datetime.date) -> bool:
    return d in federal_holidays(d.year)


def is_working_day(d: datetime.date) -> bool:
    """Monday–Friday and not an observed federal holiday."""
    return d.weekday() < 5 and not is_federal_holiday(d)


def add_working_days(start: datetime.date, n: int) -> datetime.date:
    """The date that is ``n`` working days after ``start`` (start not counted).

    A regulatory clock of 'within N working days after X' resolves to the Nth
    working day strictly after X. n must be positive.
    """
    if n < 1:
        raise ValueError("n must be a positive number of working days")
    d = start
    counted = 0
    while counted < n:
        d = d + _DAY
        if is_working_day(d):
            counted += 1
    return d


def working_days_between(start: datetime.date, end: datetime.date) -> int:
    """Count working days strictly after ``start`` up to and including ``end``."""
    if end < start:
        return -working_days_between(end, start)
    d, count = start, 0
    while d < end:
        d = d + _DAY
        if is_working_day(d):
            count += 1
    return count


@dataclass
class Deadline:
    name: str
    citation: str
    basis: str                 # "working-day" | "calendar-day"
    n: int
    anchor: datetime.date
    due: datetime.date

    def days_remaining(self, as_of: datetime.date) -> int:
        if self.basis == "working-day":
            return working_days_between(as_of, self.due)
        return (self.due - as_of).days


def expanded_access_emergency_deadlines(authorization_date: datetime.date) -> List[Deadline]:
    """The two clocks that start when FDA authorizes emergency use by phone.

    312.310(d)(2): written submission within 15 working days.
    56.104(c): IRB notification within 5 working days.
    """
    return [
        Deadline("Written expanded-access submission to FDA", "21 CFR 312.310(d)(2)",
                 "working-day", 15, authorization_date, add_working_days(authorization_date, 15)),
        Deadline("IRB notification of emergency use", "21 CFR 56.104(c)",
                 "working-day", 5, authorization_date, add_working_days(authorization_date, 5)),
    ]


def ind_30_day_deadline(fda_receipt_date: datetime.date) -> Deadline:
    """21 CFR 312.40(b)(1): the IND goes into effect 30 calendar days after FDA
    receipt (absent hold or earlier notification). The returned date is the
    IND-effective date (30 calendar days after receipt) and the earliest day
    treatment may begin absent earlier FDA notification."""
    return Deadline("IND effective (30-day wait ends)", "21 CFR 312.40(b)(1)",
                    "calendar-day", 30, fda_receipt_date, fda_receipt_date + datetime.timedelta(days=30))
