"""

till.py
=======

Print interesting time diffs between now and some future date.

Helps you plan things and set your expectations.

Usage:
    $ till jul18
    4 days from now
    $ till q4
    79 days from now

"""

import calendar
from datetime import datetime
import sys

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import humanize


now = datetime.now


def main(argv):
    if not argv:
        # till eod, eow, mon, eom, eoq, eoy
        return

    future_encoded = argv[0]

    if future_encoded == 'eod':
        future = end_of_day()
    elif future_encoded == 'eow':
        future = end_of_week()
    elif future_encoded == 'mon':
        future = next_monday()
    elif future_encoded == 'eoq':
        future = end_of_quarter()
    else:
        future = parse(future_encoded)

    interesting_deltas(future)

    # tried the following. seems a bit too limited for this use.
    print future, humanize.naturaltime(future)


def end_of_day(fixed_now=None):
    if fixed_now is None:
        fixed_now = now()

    return fixed_now.replace(hour=17, minute=0, second=0)


def end_of_week(fixed_now=None):
    if fixed_now is None:
        fixed_now = now()

    return fixed_now + relativedelta(weekday=calendar.FRIDAY)


def next_monday(fixed_now=None):
    if fixed_now is None:
        fixed_now = now()

    return fixed_now + relativedelta(days=1, weekday=calendar.MONDAY)


def end_of_quarter(fixed_now=None):
    if fixed_now is None:
        fixed_now = now()

    if fixed_now.month < 3:
        return fixed_now + relativedelta(month=3, day=31)
    if fixed_now.month < 6:
        return fixed_now + relativedelta(month=6, day=30)
    if fixed_now.month < 9:
        return fixed_now + relativedelta(month=9, day=31)
    return fixed_now + relativedelta(month=12, day=31)


def interesting_deltas(future, fixed_now=None):
    if fixed_now is None:
        fixed_now = now()

    td = future - fixed_now

    # # of days
    print "{} days".format(diff_days(td)),

    # # of weeks
    print "{:.2f} weeks".format(diff_weeks(td)),

    # # of hours
    print "{:.2f} hours".format(diff_hours(td)),

    # # of months
    print "~{:.2f} months".format(diff_months(td)),

    # # of minutes
    print "{:.2f} minutes".format(diff_minutes(td))

    # # of waking hours
    print "~{:.2f} waking hours".format(diff_waking_hours(td)),

    # # of work hours
    print "~{:.2f} work hours".format(diff_work_hours(td)),

    # # of effective work hours
    print "~{:.2f} effective work hours".format(diff_effective_work_hours(td))

    # # of workdays


def diff_days(td):
    x = td.total_seconds() / 86400  # seconds per day
    return int(round(x))


def diff_weeks(td):
    return td.total_seconds() / 604800  # seconds per week


def diff_hours(td):
    return td.total_seconds() / 3600  # seconds per hour


def diff_months(td):
    return td.total_seconds() / 2592000  # seconds per month (approx; 30 days)


def diff_minutes(td):
    return td.total_seconds() / 60  # seconds per minute


def diff_waking_hours(td):
    return (17./24) * td.total_seconds() / 3600  # seconds per hour scaled by (17/24 usable hours per day)


def diff_work_hours(td):
    return diff_weeks(td) * 5 * 8  # 5 working days per week; 8 hours per day


def diff_effective_work_hours(td):
    return diff_weeks(td) * 5 * 4  # 5 working days per week; 4 effective hours per day



if __name__ == '__main__':
    main(sys.argv[1:])

