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


def calc_costs(request, username):
    user = request.user
    if username == user.username:
        today = datetime.today()
        curr_mo = today.month
        curr_yr = today.year
        sel_mo = request.GET.get("month", curr_mo)
        sel_yr = request.GET.get("year", curr_yr)
        #! TODO Get dishwasher from Database / household settings
        dish_washer = 1
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
        total_cons *= 1000
        perc = 0.13
        if dish_washer:
            perc = 0.18
        energy = round(total_cons * perc, 1)
        data = {
            "energy": energy,
            "total": round(total_cons, 1),
            "rest": round(total_cons - energy, 1)
        }
        variables = RequestContext(request, data)
        return render_to_response("_inner_02_1.html", variables)
