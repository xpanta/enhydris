from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from iwidget.models import UserNotifications
from django.db import connection
from iwidget.models import TSTEP_HOURLY, VAR_PERIOD
from pthelma.timeseries import Timeseries as TSeries
from datetime import datetime, timedelta
from unexe.classes.Iseries import iseries
from itertools import izip
from uc_03_1.lib.common import day_start, day_end
import numpy as np
#!TODO import ugetext for internationalizing texts


@login_required
def event_history(request, username):
    user = request.user
    if user.username == username:
        y_data = None
        today = datetime.today()
        events = UserNotifications.objects.filter(user=user).order_by('-added')
        household = user.households.all()[0]

        ts_m = household.timeseries \
            .filter(time_step__id=TSTEP_HOURLY,
                    variable__id=VAR_PERIOD)[0]
        series = iseries()
        timeseries = series.readseries(ts_m)
        dates, units = izip(*timeseries)
        night_cons = 0
        day_cons = 0
        today = dates[-1]
        yesterday = today - timedelta(days=1)
        # clear units array from nan values by using '0' instead
        units1 = np.array(units)
        units1[np.isnan(units1)] = 0
        for i in range(len(dates)):
            d = dates[i].date()
            t = dates[i].time()
            if d == yesterday.date():
                if day_start <= t.hour <= day_end:  # day
                    day_cons += units1[i]
                else:  # night
                    night_cons += units1[i]
        data = {
            'yesterday': yesterday,
            "events": events,
            "night_cons": night_cons,
            "day_cons": day_cons,
        }
        variables = RequestContext(request, data)
        return render_to_response("fault_history.html", variables)


@login_required
def user_events(request, username):
    f = request.GET.get("f", "all")
    _id = request.GET.get("hide", "")
    if _id:
        try:
            event = UserNotifications.objects.get(pk=_id)
            event.read = True
            event.save()
        except UserNotifications.DoesNotExist:
            pass
    if username == request.user.username:
        user = request.user
        notifications = UserNotifications.objects.filter(user=user)
        if f == "new":
            notifications = notifications.filter(read=False)
        elif f == "old":
            notifications = notifications.filter(read=True)
        notifications = notifications.order_by("-detected")
        data = {
            "events": notifications,
        }
        variables = RequestContext(request, data)
        return render_to_response("events_table.html", variables)
    else:
        raise Http404("Not a Valid User")
