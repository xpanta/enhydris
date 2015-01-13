#from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page
from math import isnan
from itertools import izip
from datetime import datetime
from iwidget.models import TSTEP_HOURLY, VAR_PERIOD, \
    VAR_ENERGY_PERIOD, Household, EfficientAppliance
from unexe.classes.Iseries import iseries


def calculate_appliance_energy(request, username):
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
        num = selects['appl_boiler']
        if num > 0:
            water_heater = 1
        else:
            water_heater = 0
        num = selects['appl_washing']
        if num > 0:
            cloth_washer = 1
        else:
            cloth_washer = 0
        num = selects['appl_dishwasher']
        if num > 0:
            dish_washer = 1
        else:
            dish_washer = 0
        num = selects['appl_dryer']
        if num > 0:
            dryer = 1
        else:
            dryer = 0

        init = {
            "water_heater": water_heater * 13,
            "cloth_washer": cloth_washer * 3,
            "dish_washer": dish_washer * 2,
            "heating_and_cooling": 49,
            "refrigerator": 5,
            "dryer": dryer * 3,
            "lighting": 1,
            "electronics": 7,
            "other": 8,
        }

        init_total = float(sum(init.values()))

        total_cons = 0
        household = user.households.all()[0]  # get user household id
        series = iseries()
        ts_m = household.timeseries \
            .filter(time_step__id=TSTEP_HOURLY,
                    variable__id=VAR_ENERGY_PERIOD)[0]
        timeseries1 = series.readseries(ts_m)
        dates, units = izip(*timeseries1)
        for i in range(len(dates)):
            date = dates[i]
            if date.year == int(sel_yr) and date.month == int(sel_mo):
                cons = units[i]
                if isnan(cons):
                    cons = 0
                total_cons += cons
        tc = total_cons

        data = {
            "water_heater": (init["water_heater"] / init_total) * tc,
            "cloth_washer": (init["cloth_washer"] / init_total) * tc,
            "dish_washer": (init["dish_washer"] / init_total) * tc,
            "heating_and_cooling": (init["heating_and_cooling"] / init_total) * tc,
            "refrigerator": (init["refrigerator"] / init_total) * tc,
            "dryer": (init["dryer"] / init_total) * tc,
            "lighting": (init["lighting"] / init_total) * tc,
            "electronics": (init["electronics"] / init_total) * tc,
            "other": (init["other"] / init_total) * tc,
            "init_total": init_total,
            "has_water_heater": water_heater,
            "has_dish_washer": dish_washer,
            "has_dryer": dryer,
            "has_cloth_washer": cloth_washer,
            "total": total_cons,
        }

        variables = RequestContext(request, data)
        return render_to_response("_uc_02_02_chart.html", variables)
    else:
        raise Http404("Not a valid user!")
