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
from unexe.classes.Iseries import iseries


def calculate_appliance_consumption(request, username):
    user = request.user
    if username == user.username:
        today = datetime.today()
        curr_mo = today.month
        curr_yr = today.year
        sel_mo = request.GET.get("month", curr_mo)
        sel_yr = request.GET.get("year", curr_yr)

        from unexe.classes.Ihousehold import ihousehold
        household = user.households.all()[0]
        checkboxes, selects = ihousehold.getHouseholdData(household.id)
        if len(selects) < 5:
            variables = RequestContext(request, {"error": True})
            return render_to_response("error_message_hhupd.html", variables)
        num = selects['appl_shower']
        if num > 0:
            shower = 1
        else:
            shower = 0
        num = selects['appl_washing']
        if num > 0:
            washing_machine = 1
        else:
            washing_machine = 0
        num = selects['appl_dishwasher']
        if num > 0:
            dish_washer = 1
        else:
            dish_washer = 0
        num = selects['appl_bath']
        if num > 0:
            bath = 1
        else:
            bath = 0
        num = selects['appl_toilet']
        if num > 0:
            wc = 1
        else:
            wc = 0
        num = selects['appl_sink']
        if num > 0:
            tap = 1
        else:
            tap = 0
        num1 = selects['out_areas_garden']
        num2 = selects['out_areas_pervious']
        num3 = selects['out_areas_roof']
        num4 = checkboxes['pool']
        num5 = checkboxes['car_washing']
        if num1 > 0 or num2 > 0 or num3 > 0 or num4 or num5:
            outdoor = 1
        else:
            outdoor = 0

        other = 1

        wcs = {
            "wc": 0.3,
            "shower": 0.22,
            "tap": 0.35,
            "washing_machine": 0,
            "dish_washer": 0,
            "bath": 0,
            "other": 0.13,
            "outdoor": 0
        }

        total_cons = 0
        household = user.households.all()[0]  # get user household id
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
            "wc": round(wcs["wc"] * total_cons, 1),
            "shower": round(wcs["shower"] * total_cons, 1),
            "tap": round(wcs["tap"] * total_cons, 1),
            "washing_machine": round(wcs["washing_machine"] * total_cons, 1),
            "dish_washer": round(wcs["dish_washer"] * total_cons, 1),
            "bath": round(wcs["bath"] * total_cons, 1),
            "other": round(wcs["other"] * total_cons, 1),
            "outdoor": round(wcs["outdoor"] * total_cons, 1),
        }

        data = {
            "consumptions": consumptions,
            "total": round(total_cons, 1),
            "wc": wc,
            "shower": shower,
            "tap": tap,
            "washing_machine": washing_machine,
            "dish_washer": dish_washer,
            "bath": bath,
            "other": other,
            "outdoor": outdoor,
        }
        variables = RequestContext(request, data)
        return render_to_response("_chart.html", variables)
    else:
        raise Http404("Not a valid user!")
