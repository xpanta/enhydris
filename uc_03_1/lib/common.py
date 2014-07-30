__author__ = 'chris'

from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_start_date(end_date, step, period):
    if 'monthly' in step:
        if 'custom' not in period:
            ago = int(period)
            return end_date - relativedelta(months=ago)
    elif 'daily' in step:
        if '7' in period:
            return end_date - relativedelta(days=7)
        elif 'month' in period:
            return end_date.replace(day=1)


def get_custom_start_end_dates(month1, year1, month2, year2):
    d = "%s/%s" % (month1, year1)
    date1 = datetime.strptime(d, "%m/%Y")
    d = "%s/%s" % (month2, year2)
    date2 = datetime.strptime(d, "%m/%Y")
    return date1.date(), date2.date()
