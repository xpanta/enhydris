# Create your views here.
#from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.views.decorators.cache import cache_page
from math import isnan
from lib.common import get_chart_data
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_text

#@cache_page(30 * 60)  # cache for 30 minutes
@login_required
def compare(request, username):
    # cache_key = 'uc0301__%d' % str(request.GET)
    # cache_value = cache.get(cache_key)
    # if cache_value is not None:
    #     return cache_value
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
              "Sep", "Oct", "Nov", "Dec"]
    user = request.user
    step = ""
    timeseries1 = timeseries2 = None
    total_data = []
    day_data = []
    night_data = []
    summer_data = []
    winter_data = []
    total_data2 = []
    day_data2 = []
    night_data2 = []
    summer_data2 = []
    winter_data2 = []
    key_dates = []
    key_dates2 = []
    title = ""
    title2 = ""
    summer_dict = {}
    winter_dict = {}
    total_dict2 = {}
    comparison = False  # if two charts are needed
    ticks = []  # x-axis labels
    ticks2 = []  # x-axis labels
    title = ""
    view = ""
    winter_total2 = 0
    summer_total2 = 0
    winter_total = 0
    summer_total = 0
    day_total = 0
    night_total = 0
    day_total2 = 0
    night_total2 = 0
    start2 = end2 = None
    tdk2 = []
    max_val = 0  # maximum consumption (for chart1)
    max_val2 = 0  # maximum consumption (for chart2)
    cons_table_data = []  # data prepared for the consumption tables
    cons_table_data2 = []  # data prepared for the consumption tables
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
            from datetime import datetime, timedelta
            from itertools import izip
            ts_m = None
            if step == '15min':
                from iwidget.models import TSTEP_FIFTEEN_MINUTES, VAR_PERIOD
                ts_m = household.timeseries\
                    .filter(time_step__id=TSTEP_FIFTEEN_MINUTES,
                            variable__id=VAR_PERIOD)[0]
            elif step == 'hourly':
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
            elif prd_h == 'yesterday':
                end = dates[-1].date()  # last day
                yesterday = end - timedelta(days=1)
                start = yesterday
                end = yesterday
            elif prd_h == 'custom1' or prd_h == 'custom2':
                dval = request.GET.get('day1')
                day1 = datetime.strptime(dval, "%Y-%m-%d")
                start = day1.date()
                end = day1.date()
                if prd_h == 'custom2':
                    dval2 = request.GET.get('day2')
                    day2 = datetime.strptime(dval2, "%Y-%m-%d")
                    start2 = day2.date()
                    end2 = day2.date()
                    comparison = True
        elif 'monthly' in step or 'daily' in step:
            from iwidget.models import TSTEP_HOURLY, VAR_PERIOD
            from itertools import izip
            from datetime import datetime
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
                elif prd_sw in ['custom1', 'custom2']:
                    from_yr = request.GET.get('sw_styr1', end.year)
                    to_yr = request.GET.get('sw_endyr1', end.year)
                    start = datetime.today()\
                        .replace(day=1, month=1, year=int(from_yr)).date()
                    end = datetime.today()\
                        .replace(day=31, month=12, year=int(to_yr)).date()
                    if prd_sw == 'custom2':
                        from_yr = request.GET.get('sw_styr2', end.year)
                        to_yr = request.GET.get('sw_endyr2', end.year)
                        start2 = datetime.today() \
                            .replace(day=1, month=1, year=int(from_yr)).date()
                        end2 = datetime.today() \
                            .replace(day=31, month=12, year=int(to_yr)).date()
            else:
                if 'custom' not in period:
                    from lib.common import get_start_date
                    start = get_start_date(end, step, period)
                else:
                    if 'monthly' in step and \
                            (period in ['custom1', 'custom2']):
                        from lib.common import get_custom_start_end_dates
                        x1 = request.GET.get("stm1")
                        x2 = request.GET.get("sty1")
                        y1 = request.GET.get("endm1")
                        y2 = request.GET.get("endy1")
                        start, end = get_custom_start_end_dates(x1, x2, y1, y2)
                        if period == 'custom2':
                            x1 = request.GET.get("stm2")
                            x2 = request.GET.get("sty2")
                            y1 = request.GET.get("endm2")
                            y2 = request.GET.get("endy2")
                            start2, end2 = get_custom_start_end_dates(x1, x2,
                                                                      y1, y2)
                    elif 'daily' in step and period in ['custom1', 'custom2']:
                        st_date1 = request.GET.get('from1')
                        end_date1 = request.GET.get('to1')
                        start = datetime.strptime(st_date1, "%Y-%m-%d").date()
                        end = datetime.strptime(end_date1, "%Y-%m-%d").date()
                        if period == 'custom2':
                            st_date2 = request.GET.get('from2')
                            end_date2 = request.GET.get('to2')
                            start2 = datetime.strptime(st_date2,
                                                       "%Y-%m-%d").date()
                            end2 = datetime.strptime(end_date2,
                                                     "%Y-%m-%d").date()
        total_dict, night_dict, day_dict, summer_dict, \
            winter_dict = get_chart_data(household, dates, units, step,
                                         view, start, end)
        _str = _("Resolution chart")
        smart_text(_str, encoding='utf-8')
        if start == end:
            title = "{x} {s} {y}"\
                .format(x=step.title(), y=start, s=_str.encode('utf-8'))
        else:
            title = "{x} {s} {z} - {y}"\
                .format(x=step.title(), z=start, y=end, s=_str.encode('utf-8'))
        if start2 and end2:
            total_dict2, night_dict2, day_dict2, summer_dict2, \
                winter_dict2 = get_chart_data(household, dates, units, step,
                                              view, start2, end2)
            if start2 == end2:
                title2 = "{x} {s} {y}" \
                    .format(x=step.title(), y=start2, s=_str)
            else:
                title2 = "{x} {s} {z} - {y}" \
                    .format(x=step.title(), z=start2, y=end2, s=_str)
        tdk = total_dict.keys()
        if total_dict2:
            tdk2 = total_dict2.keys()
        if 'monthly' in step:
            key_dates = sorted(tdk,
                               key=lambda a: datetime.strptime(a, "%Y/%m"))
            if tdk2:
                key_dates2 = sorted(tdk2,
                                    key=lambda a: datetime.strptime(a, "%Y/%m"))
        elif 'daily' in step:
            key_dates = sorted(tdk,
                               key=lambda a:
                               datetime.strptime(a, "%Y/%m/%d"))
            if tdk2:
                key_dates2 = sorted(tdk2,
                                    key=lambda a:
                                    datetime.strptime(a, "%Y/%m/%d"))
        elif step in ['hourly', '15min']:
            key_dates = sorted(tdk,
                               key=lambda a: datetime.strptime(a, "%H:%M"))
            if tdk2:
                key_dates2 = sorted(tdk2,
                                    key=lambda a: datetime.strptime(a, "%H:%M"))
        x = 0
        # Prepare chart data to be displayed and the x-axis labels
        if step == "15min":
            key_dates = key_dates[-80:]
            if key_dates2:
                key_dates2 = key_dates2[-80:]
        for dt in key_dates:
            val = float(total_dict[dt])
            if step != "monthly":
                val *= 1000
            total_data.append([x, val])
            if val > max_val:
                max_val = val
            if view == 'day_night':
                nv = night_dict[dt]
                dv = day_dict[dt]
                if step != "monthly":
                    nv *= 1000
                    dv *= 1000
                night_data.append([x, nv])
                day_data.append([x, dv])
                night_total += nv
                day_total += dv
            elif view == 'summer_winter':
                summer_data.append([x, summer_dict[dt]])
                winter_data.append([x, winter_dict[dt]])
                summer_total += summer_dict[dt]
                winter_total += winter_dict[dt]
            if step == '15min':
                if ":00" not in dt:
                    ticks.append([x, ""])
                else:
                    ticks.append([x, dt])
            else:
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
                    arr.append(night_dict[dt] * 1000)
                    arr.append(day_dict[dt] * 1000)
                cons_table_data.append(arr)
        x = 0
        # Only if the user needs to combine two charts
        if key_dates2:
            for dt in key_dates2:
                val = float(total_dict2[dt])
                if step != "monthly":
                    val *= 1000
                total_data2.append([x, val])
                if val > max_val2:
                    max_val2 = val
                if view == 'day_night':
                    night_data2.append([x, night_dict2[dt]])
                    day_data2.append([x, day_dict2[dt]])
                    night_total2 += night_dict2[dt]
                    day_total2 += day_dict2[dt]
                elif view == 'summer_winter':
                    summer_data2.append([x, summer_dict2[dt]])
                    winter_data2.append([x, winter_dict2[dt]])
                    summer_total2 += summer_dict2[dt]
                    winter_total2 += winter_dict2[dt]
                if step == '15min':
                    if ":00" not in dt:
                        ticks2.append([x, ""])
                    else:
                        ticks2.append([x, dt])
                else:
                    ticks2.append([x, dt])
                x += 1
                # Prepare nicely data for the consumptions tables
                # remember that dt gives also date information
                if step in ["hourly", "15min"]:
                    txt = dt
                    arr = [txt, val]
                    cons_table_data2.append(arr)
                if "monthly" in step:
                    d_time = datetime.strptime(dt, "%Y/%m")
                    txt = "%s of %s" % (months[d_time.month-1],
                                        str(d_time.year))
                    arr = [txt, val]
                    if view == "day_night":
                        arr.append(night_dict2[dt])
                        arr.append(day_dict2[dt])
                    cons_table_data2.append(arr)
                if "daily" in step:
                    d_time = datetime.strptime(dt, "%Y/%m/%d")
                    txt = "%s %s, %s" % (str(d_time.day),
                                         months[d_time.month-1],
                                         str(d_time.year))
                    arr = [txt, val]
                    if view == 'day_night':
                        arr.append(night_dict2[dt] * 1000)
                        arr.append(day_dict2[dt] * 1000)
                    cons_table_data2.append(arr)
    # if view is for summer / winter then max_val should be
    # something else.
    if view == 'summer_winter':
        max_val = max(summer_total, winter_total)
        if summer_total2 and winter_total2:
            max_val2 = max(summer_total2, winter_total2)
    # last minute transformation. All data apart from monthly should be in ltr
    if step != "monthly":
        unit = "lt"
    else:
        unit = "m&#179;"
    data = {
        'unit': unit,
        'username': username,
        # 'timeseries1': timeseries1,
        'timeseries2': timeseries2,
        'total_data': total_data,
        'day_data': day_data,
        'night_data': night_data,
        'total_data2': total_data2,
        'day_data2': day_data2,
        'night_data2': night_data2,
        'ticks': ticks,
        'ticks2': ticks2,
        'title': title,
        'title2': title2,
        'view': view,
        'max_val': max_val + max_val * 0.2,  # give some space above
        'max_val2': max_val2 + max_val2 * 0.2,  # give some space above
        'cons_table_data': cons_table_data,
        'cons_table_data2': cons_table_data2,
        'night_total': night_total,
        'day_total': day_total,
        'night_total2': night_total2,
        'day_total2': day_total2,
        'summer_total': summer_total,
        'winter_total': winter_total,
        'summer_data': summer_data,
        'winter_data': winter_data,
        'summer_total2': summer_total2,
        'winter_total2': winter_total2,
        'summer_data2': summer_data2,
        'winter_data2': winter_data2,
        'step': step,
    }
    # cache.set(cache_key, result, 600)
    variables = RequestContext(request, data)
    return render_to_response("_charts_.html", variables)


