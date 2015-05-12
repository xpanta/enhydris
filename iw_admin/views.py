from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from iwidget.models import UsageData, UserPageView
from django.contrib.auth.models import User
from iwidget.models import Household, VAR_PERIOD, VAR_ENERGY_PERIOD, \
    VAR_CUMULATIVE, VAR_ENERGY_CUMULATIVE
from pthelma.timeseries import timeseries_bounding_dates_from_db
from django import db
import time

@login_required
def usage_data(request, ctr_code):
    user = request.user
    if user.is_superuser:
        users = User.objects.filter(username__startswith=ctr_code)
        u_data = {}
        user_pages = {}
        for user in users:
            arr = [user.username]
            household = Household.objects.get(user=user)
            for variable in (VAR_PERIOD, VAR_ENERGY_PERIOD):
                if variable == VAR_PERIOD:
                    _type = "WATER"
                else:
                    _type = "ENERGY"
                raw_series_db = household.timeseries.filter(
                    time_step__isnull=True,
                    variable__id={
                        VAR_PERIOD: VAR_CUMULATIVE,
                        VAR_ENERGY_PERIOD: VAR_ENERGY_CUMULATIVE
                    }[variable])[:1]
                if not raw_series_db:
                    continue
                raw_series_db = raw_series_db[0]
                s1, e1 = timeseries_bounding_dates_from_db(
                    db.connection, raw_series_db.id)
                if s1:
                    start = s1.strftime("%Y-%m-%d %H:%M")
                else:
                    start = ""
                if e1:
                    end = e1.strftime("%Y-%m-%d %H:%M")
                else:
                    end = ""
                arr.extend([start, end])
            ud = UsageData.objects.filter(user=user)
            if ud:
                ets = ud[0].enter_ts
                lts = ud[0].exit_ts
                arr.append(ets.strftime("%Y-%m-%d %H:%M"))
                arr.append(lts.strftime("%Y-%m-%d %H:%M"))
                # duration
                arr.append(int(time.mktime(lts.timetuple())
                               - time.mktime(ets.timetuple())) / 60)
            else:
                arr.extend([0, 0, 0])
            u_data[user.id] = arr
            upvs = UserPageView.objects.filter(user=user)
            pages = {}
            for upv in upvs:
                page = upv.page
                count = pages.get(page, 0)
                count += 1
                pages[page] = count
            keys = pages.keys()
            page_tuples = []
            for k in keys:
                page_tuples.append((k, pages[k]))
            user_pages[user.id] = page_tuples
        data = {
            "users": users,
            "data": u_data,
            "pages": user_pages,
        }
        variables = RequestContext(request, data)
        return render_to_response("_usage_data.html", variables)
    else:
        return HttpResponseRedirect(reverse('dashboard'))
