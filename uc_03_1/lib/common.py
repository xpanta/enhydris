__author__ = 'chris'

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext as _

day_start = 4
day_end = 24
night_start = 3
night_end = 5

def get_year_start_end(when, end):
    """
        when: current or previous year (0, -1)
    """
    yr = end - relativedelta(years=when)
    start = yr.replace(month=1, day=1)
    end = yr.replace(month=12, day=31)

    return start, end


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


def get_chart_data(household, dates, units, step, view, start, end):
    # Now that we have determined start and end dates
    # we can get the total amount of litres the household consumed
    # if we need day and night values we will need to do extra work
    # because hour data is only in hourly timeseries. We need to parse
    # hourly data and integrate them into monthly groups
    from math import isnan
    from unexe.classes.Ihousehold import ihousehold
    total_dict = {}
    summer_dict = {}
    winter_dict = {}
    winter = [1, 2, 3, 4, 9, 10, 11, 12]
    summer = [5, 6, 7, 8]
    days = [_("Mon"), _("Tue"), _("Wed"), _("Thu"), _("Fri"),
            _("Sat"), _("Sun")]
    total_dict = {}
    day_dict = {}
    night_dict = {}
    hh = ihousehold()
    for x in range(0, len(dates)):
        if start <= dates[x].date() <= end:
            hour = int(dates[x].time().hour)
            month = int(dates[x].date().month)
            if step in ['hourly', '15min']:
                ti = dates[x].time()
                key = "%02d:%02d" % (ti.hour, ti.minute)  # 02d: Two Digits
            if 'monthly' in step:
                mo = str(dates[x].date().month)
                yr = str(dates[x].date().year)
                key = "%s/%s" % (yr, mo)
            elif 'daily' in step:
                mo = str(dates[x].date().month)
                day = str(dates[x].date().day)
                yr = str(dates[x].date().year)
                key = "%s/%s/%s" % (yr, mo, day)
            consumption = float(units[x])
            if isnan(consumption):
                consumption = 0
            try:
                total_dict[key] += consumption
            except KeyError:  # if not there, put it!
                total_dict[key] = consumption
            # add day / night values if asked
            if view == 'day_night':
                if day_start <= hour <= day_end:
                    try:
                        day_dict[key] += consumption
                        night_dict[key] += 0
                    except KeyError:  # if not there, put it!
                        day_dict[key] = consumption
                        night_dict[key] = 0  # i do this 4 consistency
                else:
                    try:
                        night_dict[key] += consumption
                        day_dict[key] += 0
                    except KeyError:  # if not there, put it!
                        night_dict[key] = consumption
                        day_dict[key] = 0
            elif view == 'summer_winter':
                if month in winter:
                    try:
                        winter_dict[key] += consumption
                        summer_dict[key] += 0
                    except KeyError:  # if not there, put it!
                        winter_dict[key] = consumption
                        summer_dict[key] = 0  # i do this 4 consistency
                else:
                    try:
                        summer_dict[key] += consumption
                        winter_dict[key] += 0
                    except KeyError:  # if not there, put it!
                        summer_dict[key] = consumption
                        winter_dict[key] = 0

    # If we need monthly cost then we need to multiply consumption
    # with tarrif
    if 'cost' in step:
        for k in total_dict.keys():
            cost = hh.tariff1(total_dict[k])
            total_dict[k] = cost
        for k in day_dict.keys():
            cost = hh.tariff1(day_dict[k])
            day_dict[k] = cost
        for k in night_dict.keys():
            cost = hh.tariff1(night_dict[k])
            night_dict[k] = cost
    if 'capita' in step:
        num = household.num_of_occupants
        if num > 0:
            for k in total_dict.keys():
                per_c = total_dict[k] / float(num)
                total_dict[k] = per_c
            for k in day_dict.keys():
                per_c = day_dict[k] / float(num)
                day_dict[k] = per_c
            for k in night_dict.keys():
                per_c = night_dict[k] / float(num)
                night_dict[k] = per_c
                # We need to sort the values. What we do next is this:
                # We take the total dict keys (year/month) and we sort them
                # using strptime that takes a string and creates a datetime object.
                # This way dict values are sorted correctly and added to a list
                # for the chart to be displayed correctly.

    return total_dict, night_dict, day_dict, summer_dict, winter_dict
