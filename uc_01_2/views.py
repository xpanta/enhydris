#from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page
from math import isnan
from itertools import izip
from datetime import datetime
from iwidget.models import TSTEP_HOURLY, VAR_PERIOD


def calculate_appliance_consumption(request, username):
    user = request.user
    if username == user.username:
        today = datetime.today()
        curr_mo = today.month
        curr_yr = today.year
        sel_mo = request.GET.get("month", curr_mo)
        sel_yr = request.GET.get("year", curr_yr)
        wc = 1
        shower = 1
        tap = 2
        washing_machine = 1
        dish_washer = 0
        bath = 0
        other = 1
        outdoor = 0

        wcs = {
            "wc": 0.3,
            "shower": 0.12,
            "tap": 0.15,
            "washing_machine": 0.13,
            "dish_washer": 0.08,
            "bath": 0.1,
            "other": 0.05,
            "outdoor": 0.07
        }

        total_cons = 0
        household = user.households.all()[0]  # get user household id
        from unexe.classes.Iseries import iseries
        series = iseries()
        ts_m = household.timeseries \
            .filter(time_step__id=TSTEP_HOURLY,
                    variable__id=VAR_PERIOD)[0]
        timeseries1 = series.readseries(ts_m)
        dates, units = izip(*timeseries1)
        for i in range(len(dates)):
            date = dates[i]
            if date.year == int(sel_yr) and date.month == int(sel_mo):
                cons = units[i]
                if isnan(cons):
                    cons = 0
                total_cons += cons
        if bath:
            d = 0.1
            wcs["shower"] -= d
            wcs["bath"] += d
        if washing_machine:
            d = 0.13
            wcs["tap"] -= d
            wcs["washing_machine"] += d
        if dish_washer:
            d = 0.08
            wcs["tap"] -= d
            wcs["dish_washer"] += d
        if outdoor:
            d = 0.07
            wcs["other"] -= d
            wcs["outdoor"] += d
        total_cons *= 1000.0
        consumptions = {
            "wc": wcs["wc"] * total_cons,
            "shower": wcs["shower"] * total_cons,
            "tap": wcs["tap"] * total_cons,
            "washing_machine": wcs["washing_machine"] * total_cons,
            "dish_washer": wcs["dish_washer"] * total_cons,
            "bath": wcs["bath"] * total_cons,
            "other": wcs["other"] * total_cons,
            "outdoor": wcs["outdoor"] * total_cons,
            "total": total_cons
        }

        data = {
            "consumptions": consumptions,
            "total": total_cons,
        }
        variables = RequestContext(request, data)
        return render_to_response("_chart.html", variables)
    else:
        raise Http404("Not a valid user!")
