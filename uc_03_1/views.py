# Create your views here.
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

#!TODO import ugetext for internationalizing texts
day_start = 6
day_end = 24
night_start = 0
night_end = 6


#@cache_page(15 * 60)  # cache for 15 minutes
@login_required
def compare(request, username):
    # cache_key = 'uc0301__%d' % str(request.GET)
    # cache_value = cache.get(cache_key)
    # if cache_value is not None:
    #     return cache_value
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
              "Sep", "Oct", "Nov", "Dec"]
    winter = [1, 2, 3, 4, 9, 10, 11, 12]
    summer = [5, 6, 7, 8]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    user = request.user
    step = ""
    timeseries1 = timeseries2 = None
    total_data = []
    day_data = []
    night_data = []
    summer_data = []
    winter_data = []
    summer_dict = {}
    winter_dict = {}
    ticks = []  # x-axis labels
    title = ""
    view = ""
    winter_total = 0
    summer_total = 0
    day_total = 0
    night_total = 0
    max_val = 0  # maximum consumption (for charts)
    cons_table_data = []  # data prepared for the consumption tables
    if user.username == username:
        step = request.GET.get('step', None)
        view = request.GET.get('view', None)
        prd_m = request.GET.get('period_m', 3)
        prd_d = request.GET.get('period_d', "7days")
        if 'monthly' in step:
            period = prd_m
        elif 'daily' in step:
            period = prd_d
        else:
            period = None
        household = user.households.all()[0]  # get user household id
        dma = household.dma  # get dma of the user
        from unexe.classes.Iseries import iseries
        series = iseries()
        if step in ['15min', 'hourly']:
            from math import isnan
            from datetime import datetime, timedelta
            #from datetime import datetime, timedelta
            from itertools import izip
            ts_m = None
            if step == '15min':
                title = "15-Minute Data Resolution for {x} " \
                        "(showing only last 80 values)"
                from iwidget.models import TSTEP_FIFTEEN_MINUTES, VAR_PERIOD
                ts_m = household.timeseries\
                    .filter(time_step__id=TSTEP_FIFTEEN_MINUTES,
                            variable__id=VAR_PERIOD)[0]
            elif step == 'hourly':
                title = "Hourly Data Resolution for {x}"
                from iwidget.models import TSTEP_HOURLY, VAR_PERIOD
                ts_m = household.timeseries \
                    .filter(time_step__id=TSTEP_HOURLY,
                            variable__id=VAR_PERIOD)[0]

            timeseries1 = series.readseries(ts_m)
            # timeseries1 = timeseries1[-24:]
            dates, units = izip(*timeseries1)
            prd_h = request.GET.get('period_h', 'today')
            if prd_h == 'today':
                end = dates[-1].date()  # last day
                start = end
                title = title.format(x='Today')
            elif prd_h == 'yesterday':
                end = dates[-1].date()  # last day
                yesterday = end - timedelta(days=1)
                start = yesterday
                end = yesterday
                title = title.format(x='Yesterday')
            elif prd_h == 'custom1':
                dval = request.GET.get('day1')
                day1 = datetime.strptime(dval, "%Y-%m-%d")
                start = day1.date()
                end = day1.date()
                title = title.format(x=dval)
            elif prd_h == 'custom2':
                pass
        elif 'monthly' in step or 'daily' in step:
            from iwidget.models import TSTEP_HOURLY, VAR_PERIOD
            from unexe.classes.Ihousehold import ihousehold
            from itertools import izip
            from math import isnan
            from datetime import datetime
            hh = ihousehold()
            ts_m = household.timeseries.filter(time_step__id=TSTEP_HOURLY,
                                               variable__id=VAR_PERIOD)[0]
            timeseries1 = series.readseries(ts_m)
            # We need to find start and end dates to perform
            # consumption calculations for that dates
            dates, units = izip(*timeseries1)
            end = dates[-1].date()  # last day
            start = end  # let's initialise it first
            if view == 'summer_winter':
                from lib.common import get_year_start_end
                prd_sw = request.GET.get('period_sw', 'current')
                if 'custom' not in prd_sw:
                    param = request.GET.get('period_sw', 0)
                    val = int(param)
                    start, end = get_year_start_end(val, end)
                elif prd_sw == 'custom1':
                    from_yr = request.GET.get('sw_styr1', end.year)
                    to_yr = request.GET.get('sw_endyr1', end.year)
                    start = datetime.today()\
                        .replace(day=1, month=1, year=int(from_yr)).date()
                    end = datetime.today()\
                        .replace(day=31, month=12, year=int(to_yr)).date()
                elif prd_sw == 'custom2':
                    pass
            else:
                if 'custom' not in period:
                    from lib.common import get_start_date
                    start = get_start_date(end, step, period)
                else:
                    if 'monthly' in step and period == 'custom1':
                        from lib.common import get_custom_start_end_dates
                        x1 = request.GET.get("stm1")
                        x2 = request.GET.get("sty1")
                        y1 = request.GET.get("endm1")
                        y2 = request.GET.get("endy1")
                        start, end = get_custom_start_end_dates(x1, x2, y1, y2)
                    elif 'monthly' in step and period == 'custom2':
                        pass
                    elif 'daily' in step and period == 'custom1':
                        st_date1 = request.GET.get('from1')
                        end_date1 = request.GET.get('to1')
                        start = datetime.strptime(st_date1, "%Y-%m-%d").date()
                        end = datetime.strptime(end_date1, "%Y-%m-%d").date()
                    elif 'daily' in step and period == 'custom2':
                        pass

        # Now that we have determined start and end dates
        # we can get the total amount of litres the household consumed
        # if we need day and night values we will need to do extra work
        # because hour data is only in hourly timeseries. We need to parse
        # hourly data and integrate them into monthly groups
        total_dict = {}
        day_dict = {}
        night_dict = {}
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
        tdk = total_dict.keys()
        key_dates = []
        if 'monthly' in step:
            key_dates = sorted(tdk,
                               key=lambda a: datetime.strptime(a, "%Y/%m"))
        elif 'daily' in step:
            key_dates = sorted(tdk,
                               key=lambda a:
                               datetime.strptime(a, "%Y/%m/%d"))
        elif step in ['hourly', '15min']:
            key_dates = sorted(tdk,
                               key=lambda a: datetime.strptime(a, "%H:%M"))
        x = 0
        # Prepare chart data to be displayed and the x-axis labels
        if step == "15min":
            key_dates = key_dates[-80:]
        for dt in key_dates:
            val = float(total_dict[dt])
            total_data.append([x, val])
            if val > max_val:
                max_val = val
            if view == 'day_night':
                night_data.append([x, night_dict[dt]])
                day_data.append([x, day_dict[dt]])
                night_total += night_dict[dt]
                day_total += day_dict[dt]
            elif view == 'summer_winter':
                summer_data.append([x, summer_dict[dt]])
                winter_data.append([x, winter_dict[dt]])
                summer_total += summer_dict[dt]
                winter_total += winter_dict[dt]

            ticks.append([x, dt])
            x += 1
            # Prepare nicely data for the consumptions tables
            # remember that dt gives also date information
            if step in ["hourly", "15min"]:
                txt = dt
                arr = [txt, val]
                cons_table_data.append(arr)
            if "monthly" in step:
                d_time = datetime.strptime(dt, "%Y/%m")
                txt = "%s of %s" % (months[d_time.month-1],
                                    str(d_time.year))
                arr = [txt, val]
                if view == "day_night":
                    arr.append(night_dict[dt])
                    arr.append(day_dict[dt])
                cons_table_data.append(arr)
            if "daily" in step:
                d_time = datetime.strptime(dt, "%Y/%m/%d")
                txt = "%s %s, %s" % (str(d_time.day),
                                     months[d_time.month-1],
                                     str(d_time.year))
                arr = [txt, val]
                if view == 'day_night':
                    arr.append(night_dict[dt])
                    arr.append(day_dict[dt])
                cons_table_data.append(arr)
        # if view is for summer / winter then max_val should be
        # something else.
        if view == 'summer_winter':
            max_val = max(summer_total, winter_total)
    data = {
        'username': username,
        'timeseries1': timeseries1,
        'timeseries2': timeseries2,
        'total_data': total_data,
        'day_data': day_data,
        'night_data': night_data,
        'ticks': ticks,
        'title': title,
        'view': view,
        'max_val': max_val + max_val * 0.2,  # give some space above
        'cons_table_data': cons_table_data,
        'night_total': night_total,
        'day_total': day_total,
        'summer_total': summer_total,
        'winter_total': winter_total,
        'summer_data': summer_data,
        'winter_data': winter_data,
        'step': step,
    }
    # cache.set(cache_key, result, 600)
    variables = RequestContext(request, data)
    return render_to_response("_charts_.html", variables)


