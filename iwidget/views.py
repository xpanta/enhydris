# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Technical University of Athens

import os
import logging
from datetime import datetime, timedelta

from math import isnan
from itertools import izip
from django.utils import simplejson

from unexe.classes.Iseries import iseries
import numpy as np
from django import db
from django.db.models import Q
from django.http import (Http404, HttpResponseRedirect, HttpResponse,)
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator

from enhydris.hcore.views import (TimeseriesDetailView as TDV,
                                  bufcount, inc_month)
from enhydris.conf import settings
from iwidget.models import (IWTimeseries, Household, DMA,
                            TSTEP_FIFTEEN_MINUTES,
                            TSTEP_DAILY, TSTEP_MONTHLY, VAR_CUMULATIVE,
                            VAR_PERIOD, VAR_COST, TSTEP_HOURLY,
                            VAR_ENERGY_PERIOD, VAR_ENERGY_COST)
from iwidget.forms import HouseholdForm
from iwidget.utils import (statistics_on_daily, energy_statistics_on_daily)
from django.utils.translation import ugettext as _


class TimeseriesDetailView(TDV):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        user = request.user
        try:
            ts = IWTimeseries.objects.get(pk=object_id)
        except IWTimeseries.DoesNotExist:
            raise Http404('Timeseries object does not exist')
        is_household = hasattr(ts.gentity, 'gpoint') \
            and hasattr(ts.gentity.gpoint, 'household')
        if not (user.is_staff or user.is_superuser) and \
                (not is_household
                 or ts.gentity.gpoint.household.user.id != user.id):
            request.notifications.error("Permission denied")
            return HttpResponseRedirect(reverse('index'))
        return super(TimeseriesDetailView, self).dispatch(request,
                                                          *args, **kwargs)

@login_required
def household_view(request, household_id=None):
    user = request.user
    if not household_id:
        household = user.households.all()[0]
    else:
        try:
            household = Household.objects.get(pk=household_id)
        except Household.DoesNotExist:
            raise Http404
    if not (user.is_staff or user.is_superuser) and \
            (household.user.id != user.id):
        request.notifications.error("Permission denied")
        return HttpResponseRedirect(reverse('index'))
    dma = household.dma
    ts_dma_daily_pc = dma.timeseries.filter(
        Q(time_step__id=TSTEP_DAILY) &
        Q(name__icontains='capita') &
        Q(variable__id=VAR_PERIOD))[0]
    ts_dma_monthly_pc = dma.timeseries.filter(
        Q(time_step__id=TSTEP_MONTHLY) &
        Q(name__icontains='capita') &
        Q(variable__id=VAR_PERIOD))[0]
    ts_raw = household.timeseries.filter(time_step__isnull=True,
                                         variable__id=VAR_CUMULATIVE)[0]
    ts_fifteen = household.timeseries.filter(
        time_step__id=TSTEP_FIFTEEN_MINUTES, variable__id=VAR_PERIOD)[0]
    ts_hourly = household.timeseries.filter(
        time_step__id=TSTEP_HOURLY,
        variable__id=VAR_PERIOD)[0]
    ts_daily = household.timeseries.filter(
        time_step__id=TSTEP_DAILY,
        variable__id=VAR_PERIOD)[0]
    ts_monthly = household.timeseries.filter(
        time_step__id=TSTEP_MONTHLY,
        variable__id=VAR_PERIOD)[0]
    # ts_cost = household.timeseries.filter(
    #     time_step__id=TSTEP_MONTHLY,
    #     variable__id=VAR_COST)[:1]
    # Energy time series
    ts_daily_energy = household.timeseries.filter(
        time_step__id=TSTEP_DAILY,
        variable__id=VAR_ENERGY_PERIOD)[:1]
    ts_daily_energy = ts_daily_energy[0] if ts_daily_energy else None
    ts_hourly_energy = household.timeseries.filter(
        time_step__id=TSTEP_HOURLY,
        variable__id=VAR_ENERGY_PERIOD)[:1]
    ts_hourly_energy = ts_hourly_energy[0] if ts_hourly_energy else None
    # ts_energy_cost = household.timeseries.filter(
    #     time_step__id=TSTEP_MONTHLY,
    #     variable__id=VAR_ENERGY_COST)[:1]
    # ts_energy_cost = ts_energy_cost[0] if ts_energy_cost else None
    ts_fifteen_energy = household.timeseries.filter(
        time_step__id=TSTEP_FIFTEEN_MINUTES,
        variable__id=VAR_ENERGY_PERIOD)[:1]
    ts_fifteen_energy = ts_fifteen_energy[0] if ts_fifteen_energy else None
    ts_monthly_energy = household.timeseries.filter(
        time_step__id=TSTEP_MONTHLY,
        variable__id=VAR_ENERGY_PERIOD)[:1]
    ts_monthly_energy = ts_monthly_energy[0] if ts_monthly_energy else None
    ts_dma_daily_energy_pc = dma.timeseries.filter(
        Q(time_step__id=TSTEP_DAILY) &
        Q(name__icontains='capita') &
        Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_dma_daily_energy_pc = ts_dma_daily_energy_pc[0] if ts_dma_daily_energy_pc else None
    ts_dma_monthly_energy_pc = dma.timeseries.filter(
        Q(time_step__id=TSTEP_MONTHLY) &
        Q(name__icontains='capita') &
        Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_dma_monthly_energy_pc = ts_dma_monthly_energy_pc[0] if \
        ts_dma_monthly_energy_pc else None

    # if len(ts_cost):
    #     ts_cost = ts_cost[0]
    # else:
    #     # Fallback
    #     ts_cost = ts_monthly
    nocc = household.num_of_occupants
    charts = [
        {
            'id': 1,
            'name': _('Fifteen minutes water consumption (litres)'),
            'display_min': False, 'display_max': True, 'display_avg': False,
            'display_sum': True, 'time_span': 'day', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'main_timeseries_id': ts_fifteen.id,
            'span_options': [_('month'), _('week'), _('day')],
        },
        {
            'id': 7,
            'name': _('Hourly water consumption (litres)'),
            'display_min': False, 'display_max': True, 'display_avg': False,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': True,
            'main_timeseries_id': ts_hourly.id,
            'has_pie': 1,
            'span_options': [_('year'), _('month'), _('week'), _('day')],
        },
        {
            'id': 6,
            'name': _('Cumulative consumption - raw measurements (m<sup>3</sup>)'),
            'display_min': False, 'display_max': False, 'display_avg': False,
            'display_sum': False, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'main_timeseries_id': ts_raw.id,
            'span_options': [_('month'), _('week'), _('day')],
        },
        'Fifteen energy placeholder',
        'Hourly energy placeholder',
        {
            'id': 2,
            'name': _('Daily water consumption (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'month', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': True,
            'main_timeseries_id': ts_daily.id, 'occupancy': nocc,
            'span_options': [_('year'), _('month'), _('week')],
        },
        {
            'id': 3,
            'name': _('Daily water consumption per capita (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'month', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'span_options': [_('year'), _('month'), _('week')],
        },
        'Daily energy placeholder',
        'Daily energy per capita placeholder',
        {
            'id': 4,
            'name': _('Water consumption per month, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': True,
            'main_timeseries_id': ts_monthly.id, 'occupancy': nocc,
            'has_pie': 2,
            'span_options': [],
        },
        {
            'id': 8,
             # 'name': u'Water cost per month, up to a year period (€)',
             # 'display_min': True, 'display_max': True, 'display_avg': True,
             # 'display_sum': True, 'time_span': 'year', 'is_vector': False,
             # 'has_stats': True, 'can_zoom': True, 'has_info_box': True,
             # 'display_lastvalue': True,
             # 'initial_display': False,
             # 'main_timeseries_id': ts_cost.id, 'occupancy': nocc,
             # 'span_options': [],
        },
        {
            'id': 5,
            'name': _('Water consumption per month, per capita, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False, 
            'span_options': [],
        },
        'Monthly energy placeholder',
        # 'Monthly energy cost placeholder',
        'Monthly energy per capita placeholder',
    ]
    if ts_daily_energy:
        # There are energy time series, add them to the array
        index = charts.index('Daily energy placeholder')
        charts[index] = \
            {
                'id': 9,
                'name': _('Daily energy consumption (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'month', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_daily_energy.id, 'occupancy': nocc,
                'span_options': [_('year'), _('month'), _('week')],
            }

        index = charts.index('Fifteen energy placeholder')
        charts[index] = \
            {
                'id': 10,
                'name': _('Fifteen minutes energy consumption (kWh)'),
                'display_min': False, 'display_max': True, 'display_avg': False,
                'display_sum': True, 'time_span': 'day', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_fifteen_energy.id,
                'span_options': [_('month'), _('week'), _('day')],
            }

        index = charts.index('Hourly energy placeholder')
        charts[index] = \
            {
                'id': 11,
                'name': _('Hourly energy consumption (kWh)'),
                'display_min': False,
                'display_max': True, 'display_avg': False,
                'display_sum': True, 'time_span': 'week', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_hourly_energy.id,
                'has_pie': 3,
                'span_options': [_('year'), _('month'), _('week'), _('day')],
            }

        index = charts.index('Daily energy per capita placeholder')
        charts[index] = \
            {
                'id': 12,
                'name': _('Daily energy consumption per capita (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'month', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'span_options': [_('year'), _('month'), _('week')],
            }

        index = charts.index('Monthly energy placeholder')
        charts[index] = \
            {
                'id': 13,
                'name': _('Monthly energy consumption (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'year', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_monthly_energy.id, 'occupancy': nocc,
                'has_pie': 4,
                'span_options': [],
            }

        index = charts.index('Monthly energy cost placeholder')
        charts[index] =\
            {
                'id': 14,
                # 'name': u'Energy cost per month, up to a year period (€)',
                # 'display_min': True, 'display_max': True, 'display_avg': True,
                # 'display_sum': True, 'time_span': 'year', 'is_vector': False,
                # 'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                # 'display_lastvalue': True,
                # 'initial_display': False,
                # 'main_timeseries_id': ts_energy_cost.id, 'occupancy': nocc,
                # 'span_options': [],
            }

        index = charts.index('Monthly energy per capita placeholder')
        charts[index] =\
            {
                'id': 15,
                # 'name': 'Montlhly energy consumption per capita (kWh)',
                # 'display_min': True, 'display_max': True, 'display_avg': True,
                # 'display_sum': True, 'time_span': 'year', 'is_vector': False,
                # 'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                # 'display_lastvalue': True,
                # 'initial_display': False,
                # 'span_options': [],
            }
    else:
        for placeholder in (
                'Fifteen energy placeholder',
                'Hourly energy placeholder',
                'Daily energy placeholder',
                'Daily energy per capita placeholder',
                'Monthly energy placeholder',
                # 'Monthly energy cost placeholder',
                'Monthly energy per capita placeholder',
                
        ):
            charts.remove(placeholder)

    # chart_selectors items:
    # key: id: the id attribue of chart instance in above chart list
    #          Select input element will be above the chart
    # value: selections: a list of ('chart_id', 'Displayed name')
    #        title: a category title to display
    #        default: default item from selections
    chart_selectors = {
            1: {
                'selections': [(1, _('Fifteen minutes water consumption')),
                               (7, _('Hourly water consumption')),
                               (6, _('Raw measurements')), ],
                'title': _('High resolution data'),
                'default': 7
            },
            2: {
                'selections': [(2, _('Daily water consumption')),
                               (3, _('Daily water consumption per capita')), ],
                'title': _('Daily data'),
                'default': 2
            },
            4: {
                'selections': [(4, _('Monthly water consumption')),
                               # (8, 'Monthly water cost'),
                               (5, _('Monthly water consumption per capita')), ],
                'title': _('Monthly data'),
                'default': 4
            },
    }

    if ts_daily_energy:
        # There are energy time series, add them to selectors
        chart_selectors[1]['selections'] += [
            (10, _('Fifteen minutes energy consumption')),
            (11, _('Hourly energy consumption')), ]
        chart_selectors[2]['selections'] += [
            (9, _('Daily energy consumption')),
            (12, _('Daily energy consumption per capita')), ]
        chart_selectors[4]['selections'] += [
            (13, _('Monthly energy consumption')),
            # (14, 'Monthly energy cost'),
            (15, _('Monthly energy consumption per capita')), ]

    variables = [
        {
            'id': 1, 'chart_id': 1, 'name': 'var_name',
            'timeseries_id': ts_fifteen.id,
            'is_bar': True, 'bar_width': 7*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 2, 'chart_id': 2, 'name': 'var_name',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 3, 'chart_id': 4, 'name': 'var_name',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1,
        },
        {
            'id': 4, 'chart_id': 6, 'name': 'var_name',
            'timeseries_id': ts_raw.id,
            'is_bar': False,
            'factor': 1.000,
        },
        {
            'id': 5, 'chart_id': 3, 'name': 'Household',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000/nocc,
        },
        {
            'id': 6, 'chart_id': 3, 'name': 'DMA',
            'timeseries_id': ts_dma_daily_pc.id,
            'factor': 1000.000,
        },
        {
            'id': 7, 'chart_id': 5, 'name': 'Household',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000/nocc,
        },
        {
            'id': 8, 'chart_id': 5, 'name': 'DMA',
            'timeseries_id': ts_dma_monthly_pc.id,
            'factor': 1.000,
        },
        {
            'id': 9, 'chart_id': 7, 'name': 'var_name',
            'timeseries_id': ts_hourly.id,
            'is_bar': True, 'bar_width': 30*60*1000,
            'factor': 1000.000,
        },
        # {
        #     'id': 10, 'chart_id': 8, 'name': 'var_name',
        #     'timeseries_id': ts_cost.id,
        #     'is_bar': True, 'bar_width': 14*24*60*60*1000,
        #     'factor': 1,
        # },
    ]
    if ts_daily_energy:
        # There are energy time series, add them to variables
        variables += [
            {
                'id': 11, 'chart_id': 9, 'name': 'Household',
                'timeseries_id': ts_daily_energy.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1.0,
            },
            {
                'id': 12, 'chart_id': 10, 'name': 'var_name',
                'timeseries_id': ts_fifteen_energy.id,
                'is_bar': True, 'bar_width': 7*60*1000,
                'factor': 1.0,
            },
            {
                'id': 13, 'chart_id': 11, 'name': 'var_name',
                'timeseries_id': ts_hourly_energy.id,
                'is_bar': True, 'bar_width': 30*60*1000,
                'factor': 1.0,
            },
            {
                'id': 14, 'chart_id': 12, 'name': 'Household',
                'timeseries_id': ts_daily_energy.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1.0/nocc,
            },
            {
                'id': 15, 'chart_id': 12, 'name': 'DMA',
                'timeseries_id': ts_dma_daily_energy_pc.id,
                'factor': 1.000,
            },
            {
                'id': 16, 'chart_id': 13, 'name': 'var_name',
                'timeseries_id': ts_monthly_energy.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': 1,
            },
            # {
            #     'id': 17, 'chart_id': 14, 'name': 'var_name',
            #     'timeseries_id': ts_energy_cost.id,
            #     'is_bar': True, 'bar_width': 14*24*60*60*1000,
            #     'factor': 1,
            # },
            {
                'id': 18, 'chart_id': 15, 'name': 'Household',
                'timeseries_id': ts_monthly_energy.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': 1.000/nocc,
            },
            {
                'id': 19, 'chart_id': 15, 'name': 'DMA',
                'timeseries_id': ts_dma_monthly_energy_pc.id,
                'factor': 1.000,
            },
        ]

    pies = {
        1: {'timeseries_id': ts_hourly.id,
            'period_unit': 'hour',
            'period_from': 1,
            'period_to': 4,
            'default_period': 'Nightly consumption 1:00-04:00',
            'alternate_period': 'Daily consumption 04:01-24:59'},
        2: {'timeseries_id': ts_monthly.id,
            'period_unit': 'month',
            'period_from': 5,
            'period_to': 9,
            'default_period': 'Summer consumption (May-September)',
            'alternate_period': 'Winter consumption (October-April)'}
    }
    if ts_daily_energy:
        # There are energy time series, add them to pies
        pies.update({
                    3: {'timeseries_id': ts_hourly_energy.id,
                        'period_unit': 'hour',
                        'period_from': 1,
                        'period_to': 4,
                        'default_period': 'Nightly consumption 1:00-04:00',
                        'alternate_period': 'Daily consumption 04:01-24:59'},
                    4: {'timeseries_id': ts_monthly_energy.id,
                        'period_unit': 'month',
                        'period_from': 5,
                        'period_to': 9,
                        'default_period': 'Summer consumption (May-September)',
                        'alternate_period': 'Winter consumption (October-April)'}
            })

    js_data = {
            'timeseries_data_url': reverse('timeseries_data'),
            'periods_stats_url': reverse('periods_stats'),
            'charts': charts,
            'variables': variables,
            'pies': pies
    }
    js_data = simplejson.dumps(js_data)
    form = HouseholdForm(instance=household)
    for field in form.fields:                
        form.fields[field].required = False
        form.fields[field].widget.attrs['disabled'] = 'disabled'
        form.fields[field].help_text=u''
    context = {'household': household,
               'charts': charts,
               'form': form,
               'js_data': js_data,
               'chart_selectors': chart_selectors,
               'overview': statistics_on_daily(ts_daily, nocc),
               'energy_overview': None}
    if ts_daily_energy:
        context['energy_overview'] = energy_statistics_on_daily(
                ts_daily_energy, nocc)
    return render_to_response('household.html',
            context,
        context_instance=RequestContext(request))

@login_required
def dma_view(request, dma_id):
    user = request.user
    if not (user.is_staff or user.is_superuser):
        request.notifications.error("Permission denied")
        return HttpResponseRedirect(reverse('index'))
    try:
        dma = DMA.objects.get(pk=dma_id)
    except DMA.DoesNotExist:
        raise Http404('DMA does not exist')
    ts_daily = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            ~Q(name__icontains='capita') & Q(variable__id=VAR_PERIOD))[0]
    ts_monthly = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            ~Q(name__icontains='capita') & Q(variable__id=VAR_PERIOD))[0]
    ts_daily_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            Q(name__icontains='capita') & Q(variable__id=VAR_PERIOD))[0]
    ts_monthly_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            Q(name__icontains='capita') & Q(variable__id=VAR_PERIOD))[0]

    ts_daily_energy = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            ~Q(name__icontains='capita') & Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_daily_energy = ts_daily_energy[0] if ts_daily_energy else None
    ts_monthly_energy = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            ~Q(name__icontains='capita') & Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_monthly_energy = ts_monthly_energy[0] if ts_monthly_energy else None
    ts_daily_energy_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            Q(name__icontains='capita') & Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_daily_energy_pc = ts_daily_energy_pc[0] if ts_daily_energy_pc else None
    ts_monthly_energy_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            Q(name__icontains='capita') & Q(variable__id=VAR_ENERGY_PERIOD))[:1]
    ts_monthly_energy_pc = ts_monthly_energy_pc[0] if ts_monthly_energy_pc else None

    charts = [
        {
            'id': 1,
            'name': _('Daily water consumption (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_daily.id,
            'span_options': [_('year'), _('month'), _('week')],
            'initial_display': True,
        },
        {
            'id': 2,
            'name': _('Water consumption per month, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_monthly.id,
            'span_options': [],
            'initial_display': True,
        },
        {
            'id': 3,
            'name': _('Daily water consumption per capita (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_daily_pc.id,
            'span_options': [_('year'), _('month'), _('week')],
            'initial_display': True,
        },
        {
            'id': 4,
            'name': _('Water consumption per month, up to a year period, per capita (<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_monthly_pc.id,
            'span_options': [],
            'initial_display': True,
        },
    ]
    if ts_daily_energy:
        charts += [
            {
                'id': 5,
                'name': _('Daily energy consumption (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'week', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'main_timeseries_id': ts_daily_energy.id,
                'span_options': [_('year'), _('month'), _('week')],
                'initial_display': True,
            },
            {
                'id': 6,
                'name': _('Energy consumption per month, up to a year period (MWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'year', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'main_timeseries_id': ts_monthly_energy.id,
                'span_options': [],
                'initial_display': True,
            },
            {
                'id': 7,
                'name': _('Daily energy consumption per capita (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'week', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'main_timeseries_id': ts_daily_energy_pc.id,
                'span_options': [_('year'), _('month'), _('week')],
                'initial_display': True,
            },
            {
                'id': 8,
                'name': _('Energy consumption per month, up to a year period, per capita (kWh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'year', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'main_timeseries_id': ts_monthly_energy_pc.id,
                'span_options': [],
                'initial_display': True,
            },
        ]

    variables = [
        {
            'id': 1, 'chart_id': 1, 'name': 'var_name',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1.000,
        },
        {
            'id': 2, 'chart_id': 2, 'name': 'var_name',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000,
        },
        {
            'id': 3, 'chart_id': 3, 'name': 'var_name',
            'timeseries_id': ts_daily_pc.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 4, 'chart_id': 4, 'name': 'var_name',
            'timeseries_id': ts_monthly_pc.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000,
        },
    ]
    if ts_daily_energy:
        variables += [
            {
                'id': 5, 'chart_id': 5, 'name': 'var_name',
                'timeseries_id': ts_daily_energy.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1.000,
            },
            {
                'id': 6, 'chart_id': 6, 'name': 'var_name',
                'timeseries_id': ts_monthly_energy.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': .001,
            },
            {
                'id': 7, 'chart_id': 7, 'name': 'var_name',
                'timeseries_id': ts_daily_energy_pc.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1.000,
            },
            {
                'id': 8, 'chart_id': 8, 'name': 'var_name',
                'timeseries_id': ts_monthly_energy_pc.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': 1.000,
            },
        ]

    js_data = \
        {
            'timeseries_data_url': reverse('timeseries_data'),
            'charts': charts,
            'variables': variables
        }
    js_data = simplejson.dumps(js_data)
    return render_to_response('dma.html',
            {'dma': dma,
             'charts': charts,
             'js_data': js_data},
        context_instance=RequestContext(request))

@login_required
def super_index(request):
    return render_to_response('superuser.html',
                              {'dmas': DMA.objects.all()},
                              context_instance=RequestContext(request))

@login_required
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    if not (request.user.is_superuser or request.user.is_staff):
        return household_view(request)
    return super_index(request)

@login_required
def household_properties(request):
    user = request.user
    household = user.households.all()
    if household.count()<1:
        raise Http404('User does not have household')
    household = household[0]
    if request.method == "POST":
        form = HouseholdForm(request.POST, request.FILES, instance=household)
        if form.is_valid():
            form.save()
            messages.success(request, _('Changes saved successfully'))
            return HttpResponseRedirect(household.get_absolute_url() +
                                        '#characteristicstab')
    else:
        form = HouseholdForm(instance=household)
    return render_to_response('household_properties_form.html',
            {'form': form,
             'household': household,
             },
        context_instance=RequestContext(request))

import linecache
from enhydris.hcore.tstmpupd import update_ts_temp_file
from pthelma.timeseries import datetime_from_iso

def periods_distribution(request, *args, **kwargs):

    def date_at_pos(pos):
        s = linecache.getline(afilename, pos)
        return datetime_from_iso(s.split(',')[0])

    def timedeltadivide(a, b):
        """Divide timedelta a by timedelta b."""
        a = a.days*86400+a.seconds
        b = b.days*86400+b.seconds
        return float(a)/float(b)

# Return the nearest record number to the specified date
# The second argument is 0 for exact match, -1 if no
# exact match and the date is after the record found,
# 1 if no exact match and the date is before the record.
    def find_line_at_date(adatetime, totlines):
        if totlines < 2:
            return totlines
        i1, i2 = 1, totlines
        d1 = date_at_pos(i1)
        d2 = date_at_pos(i2)
        if adatetime <= d1:
            return (i1, 0 if d1 == adatetime else 1)
        if adatetime >= d2:
            return (i2, 0 if d2 == adatetime else -1)
        while True:
            i = i1 + int(round(float(i2-i1) * timedeltadivide(adatetime-d1,
                                                              d2-d1)))
            d = date_at_pos(i)
            if d == adatetime:
                return (i, 0)
            if (i == i1) or (i == i2):
                return (i, -1 if i==i1 else 1)
            if d < adatetime:
                d1, i1 = d, i
            if d > adatetime:
                d2, i2 = d, i

    gstats = {'default_period': 0, 'alternate_period': 0}

    def add_to_stats(params, date, value):
        test_component = getattr(date, params['period_unit'])
        try:
            period_from = int(params['period_from'])
            period_to = int(params['period_to'])
        except ValueError:
            return
        if period_from <= test_component <= period_to:
            key = 'default_period'
        else:
            key = 'alternate_period'
        gstats[key] += value
            
    def inc_datetime(adate, unit, steps):
        if unit == 'day':
            return adate+steps * timedelta(days=1)
        elif unit == 'week':
            return adate + steps * timedelta(weeks=1)
        elif unit == 'month':
            return inc_month(adate, steps)
        elif unit == 'year':
            return inc_month(adate, 12*steps)
        elif unit == 'moment':
            return adate            
        elif unit == 'hour':
            return adate+steps * timedelta(minutes=60)
        elif unit == 'twohour':
            return adate+steps * timedelta(minutes=120)
        else:
            raise Http404
   
    if not (request.method == "GET" and request.GET.get('object_id')):
        raise Http404
    response = HttpResponse(content_type='application/json')
    response.status_code = 200
    try:
        object_id = int(request.GET['object_id'])
    except ValueError:
        raise Http404
    afilename = os.path.join(settings.ENHYDRIS_TS_GRAPH_CACHE_DIR,
                             '%d.hts'%(object_id,))
    update_ts_temp_file(settings.ENHYDRIS_TS_GRAPH_CACHE_DIR,
                        db.connection, object_id)
    chart_data = []
    if request.GET.has_key('start_pos') and request.GET.has_key('end_pos'):
        start_pos = int(request.GET['start_pos'])
        end_pos = int(request.GET['end_pos'])
    else:
        end_pos = bufcount(afilename)
        tot_lines = end_pos
        if 'last' in request.GET.keys():
            if 'date' in request.GET.keys() and request.GET['date']:
                datetimestr = request.GET['date']
                datetimefmt = '%Y-%m-%d'
                if 'time' in request.GET.keys() and request.GET['time']:
                    datetimestr = datetimestr + ' '+request.GET['time']
                    datetimefmt = datetimefmt + ' %H:%M'
                try:
                    first_date = datetime.strptime(datetimestr, datetimefmt)
                    last_date = inc_datetime(first_date, request.GET['last'], 1)
                    (end_pos, is_exact) = find_line_at_date(last_date,
                                                            tot_lines)
                    if 'exact_datetime' in request.GET.keys():
                        if request.GET['exact_datetime'] == 'true':
                            if is_exact != 0:
                                raise Http404
                except ValueError:
                    raise Http404
            else:
                last_date = date_at_pos(end_pos)
                first_date = inc_datetime(last_date, request.GET['last'], -1)
# This is an almost bad workarround to exclude the first record from
# sums, i.e. when we need the 144 10 minute values from a day.
                if 'start_offset' in request.GET.keys():
                    offset = float(request.GET['start_offset'])
                    first_date += timedelta(minutes=offset)
            start_pos = find_line_at_date(first_date, tot_lines)[0]
        else:
            start_pos = 1
    params = {x: request.GET.get(x) for x in ('period_unit',
                                              'period_from', 'period_to', )}
    if not all(params.values()):
        raise Http404
    if not params['period_unit'] in ('month', 'hour'):
        raise Http404
    length = end_pos - start_pos + 1
    fine_step = 1
    pos=start_pos
    amax=''
    prev_pos=-1
    tick_pos=-1
    afloat = 0.01
    try:
        linecache.checkcache(afilename)
        while pos < start_pos+length:
            s = linecache.getline(afilename, pos)
            if s.isspace():
                pos+=fine_step
                continue 
            t = s.split(',') 
# Use the following exception handling to catch incoplete
# reads from cache. Tries only one time, next time if
# the error on the same line persists, it raises.
            try:
                k = datetime_from_iso(t[0])
                v = t[1]
            except:
                if pos>prev_pos:
                    prev_pos = pos
                    linecache.checkcache(afilename)
                    continue
                else:
                    raise
            if v != '':
                afloat = float(v)
                add_to_stats(params, k, afloat)
# Some times linecache tries to read a file being written (from 
# timeseries.write_file). So every 5000 lines refresh the cache.
            if (pos-start_pos) % 5000 == 0:
                linecache.checkcache(afilename)
            pos += fine_step
    finally:
        linecache.clearcache()
    response.content = simplejson.dumps({'stats': gstats})
    callback = request.GET.get("jsoncallback", None)    
    if callback:
        response.content = '%s(%s)' % (callback, response.content,)
    return response


def test(request):
    logging.debug("test!!")
    return HttpResponse("OK")

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''Following are added by Adeel (14 march 2014''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
Following piece of code is duplicated to use the existing views without making any changed to the main django_iwidget application. Views logic is impossible to reuse as they all
return values to specific .html file templates. Therefore it is decided to duplicate the code in order to get the return value from logic implemented inside view rather
changing someone else which usually becomes issue to trouble shoot.
'''

'''
Following methods is the copy of def household_view(request, household_id=None) except this method return values not to template. The only change done is the return and two lines in the code
to resolve the URL
'''
def dashboard_view(request, household_id=None):
    user = request.user
    if not household_id:
        household = user.households.all()[0]
    else:
        try:
            household = Household.objects.get(pk=household_id)
        except Household.DoesNotExist:
            raise Http404
    if not (user.is_staff or user.is_superuser) and \
            (household.user.id != user.id):
        request.notifications.error(_("Permission denied"))
        return HttpResponseRedirect(reverse('index'))

    dma = household.dma
    ts_dma_daily_pc = dma.timeseries.filter(
            Q(time_step__id=TSTEP_DAILY) &
            Q(name__icontains='capita'))[0]
    ts_dma_monthly_pc = dma.timeseries.filter(
            Q(time_step__id=TSTEP_MONTHLY) &
            Q(name__icontains='capita'))[0]
    ts_raw = household.timeseries.filter(time_step__isnull=True,
            variable__id=VAR_CUMULATIVE)[0]
    ts_fifteen = household.timeseries.filter(
            time_step__id=TSTEP_FIFTEEN_MINUTES,
            variable__id=VAR_PERIOD)[0]
    ts_hourly = household.timeseries.filter(
            time_step__id=TSTEP_HOURLY,
            variable__id=VAR_PERIOD)[0]
    ts_daily = household.timeseries.filter(
            time_step__id=TSTEP_DAILY,
            variable__id=VAR_PERIOD)[0]
    ts_monthly = household.timeseries.filter(
            time_step__id=TSTEP_MONTHLY,
            variable__id=VAR_PERIOD)[0]
    # ts_cost = household.timeseries.filter(
    #         time_step__id=TSTEP_MONTHLY,
    #         variable__id=VAR_COST)[:1]

    # ENERGY DATA ADDED By Chris Pantazis
    has_energy = False
    try:
        ts_fifteen_nrg = household.timeseries.filter(
            time_step__id=TSTEP_FIFTEEN_MINUTES,
            variable__id=VAR_ENERGY_PERIOD)[0]
        # Energy Exists. Try to check if all values are 0
        series = iseries()
        timeseries1 = series.readseries(ts_fifteen_nrg)
        dates, units = izip(*timeseries1)
        units1 = np.array(units)
        units1[np.isnan(units1)] = 0
        nrg_sum = sum(units1)
        if nrg_sum < 1.0:
            has_energy = False
        else:
            has_energy = True
    except (IndexError, ValueError):
        has_energy = False

    if has_energy:
        ts_hourly_nrg = household.timeseries.filter(
            time_step__id=TSTEP_HOURLY,
            variable__id=VAR_PERIOD)[0]
        ts_daily_nrg = household.timeseries.filter(
            time_step__id=TSTEP_DAILY,
            variable__id=VAR_ENERGY_PERIOD)[0]
        ts_monthly_nrg = household.timeseries.filter(
            time_step__id=TSTEP_MONTHLY,
            variable__id=VAR_ENERGY_PERIOD)[0]
        # ts_cost_nrg = household.timeseries.filter(
        #     time_step__id=TSTEP_MONTHLY,
        #     variable__id=VAR_ENERGY_COST)[:1]
        # if len(ts_cost_nrg):
        #     ts_cost_nrg = ts_cost_nrg[0]
        # else:
        #     # Fallback
        #     ts_cost = ts_monthly_nrg
    # if len(ts_cost):
    #     ts_cost = ts_cost[0]
    # else:
    #     # Fallback
    #     ts_cost = ts_monthly
    nocc = household.num_of_occupants
    charts = [
        {
            'id': 1,
            'name': _('Fifteen minutes water consumption (litres)'),
            'display_min': False, 'display_max': True, 'display_avg': False,
            'display_sum': True, 'time_span': 'day', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': True,
            'main_timeseries_id': ts_fifteen.id,
            'span_options': [_('month'), _('week'), _('day')],
        },
        {
            'id': 7,
            'name': _('Hourly water consumption (litres)'),
            'display_min': False, 'display_max': True, 'display_avg': False,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'main_timeseries_id': ts_hourly.id,
            'has_pie': 1,
            'span_options': [_('year'), _('month'), _('week'), _('day')],
        },
        {
            'id': 6,
            'name': _('Cumulative consumption - raw measurements (m<sup>3</sup>)'),
            'display_min': False, 'display_max': False, 'display_avg': False,
            'display_sum': False, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'main_timeseries_id': ts_raw.id,
            'span_options': [_('month'), _('week'), _('day')],
        },
        {
            'id': 2,
            'name': _('Daily water consumption (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'month', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': True,
            'main_timeseries_id': ts_daily.id, 'occupancy': nocc,
            'span_options': [_('year'), _('month'), _('week')],
        },
        {
            'id': 3,
            'name': _('Daily water consumption per capita (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'month', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'span_options': [_('year'), _('month'), _('week')],
        },
        {
            'id': 4,
            'name': _('Water consumption per month, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'main_timeseries_id': ts_monthly.id, 'occupancy': nocc,
            'has_pie': 2,
            'span_options': [],
        },
        # {
        #     'id': 8,
        #     'name': u'Water cost per month, up to a year period (€)',
        #     'display_min': True, 'display_max': True, 'display_avg': True,
        #     'display_sum': True, 'time_span': 'year', 'is_vector': False,
        #     'has_stats': True, 'can_zoom': True, 'has_info_box': True,
        #     'display_lastvalue': True,
        #     'initial_display': True,
        #     'main_timeseries_id': ts_cost.id, 'occupancy': nocc,
        #     'span_options': [],
        # },
        {
            'id': 5,
            'name': _('Water consumption per month, per capita, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'initial_display': False,
            'span_options': [],
        },
    ]
    # Energy Charts added by Chris Pantazis
    charts_nrg = []
    if has_energy:
        charts_nrg = [
            {
                'id': 10,
                'name': _('Fifteen minutes energy consumption (Wh)'),
                'display_min': False, 'display_max': True, 'display_avg': False,
                'display_sum': True, 'time_span': 'day', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': True,
                'main_timeseries_id': ts_fifteen_nrg.id,
                'span_options': [_('month'), _('week'), _('day')],
            },
            {
                'id': 11,
                'name': _('Daily energy consumption (Wh)'),
                'display_min': False, 'display_max': True, 'display_avg': False,
                'display_sum': True, 'time_span': 'day', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': True,
                'main_timeseries_id': ts_daily_nrg.id,
                'span_options': [_('month'), _('week'), _('day')],
            },
            {
                'id': 12,
                # 'name': 'Energy Cost per Month (€)',
                # 'display_min': False, 'display_max': True, 'display_avg': False,
                # 'display_sum': True, 'time_span': 'day', 'is_vector': False,
                # 'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                # 'display_lastvalue': True,
                # 'initial_display': True,
                # 'main_timeseries_id': ts_cost_nrg.id,
                # 'span_options': ['month', 'week', 'day'],
            },
            {
                'id': 13,
                'name': _('Hourly energy consumption (Wh)'),
                'display_min': False, 'display_max': True, 'display_avg': False,
                'display_sum': True, 'time_span': 'week', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_hourly_nrg.id,
                'has_pie': 3,
                'span_options': [_('year'), _('month'), _('week'), _('day')],
            },
            {
                'id': 14,
                'name': _('Cumulative consumption - raw measurements (KWh)'),
                'display_min': False, 'display_max': False, 'display_avg': False,
                'display_sum': False, 'time_span': 'week', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'main_timeseries_id': ts_raw.id,
                'span_options': [_('month'), _('week'), _('day')],
            },
            {
                'id': 15,
                'name': _('Daily energy consumption per capita (Wh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'month', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'span_options': [_('year'), _('month'), _('week')],
            },
            {
                'id': 16,
                # 'name': u'Energy cost per month, up to a year period (€)',
                # 'display_min': True, 'display_max': True, 'display_avg': True,
                # 'display_sum': True, 'time_span': 'year', 'is_vector': False,
                # 'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                # 'display_lastvalue': True,
                # 'initial_display': True,
                # 'main_timeseries_id': ts_cost_nrg.id, 'occupancy': nocc,
                # 'span_options': [],
            },
            {
                'id': 17,
                'name': _('Energy consumption per month, per capita, up to a year period (Wh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'year', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': False,
                'span_options': [],
            },
            {
                'id': 18,
                'name': _('Energy consumption per month, up to a year period (Wh)'),
                'display_min': True, 'display_max': True, 'display_avg': True,
                'display_sum': True, 'time_span': 'year', 'is_vector': False,
                'has_stats': True, 'can_zoom': True, 'has_info_box': True,
                'display_lastvalue': True,
                'initial_display': True,
                'main_timeseries_id': ts_monthly_nrg.id, 'occupancy': nocc,
                'has_pie': 4,
                'span_options': [],
            },
        ]
    # chart_selectors items:
    # key: id: the id attribute of chart instance in above chart list
    #          Select input element will be above the chart
    # value: selections: a list of ('chart_id', 'Displayed name')
    #        title: a category title to display
    #        default: default item from selections
    chart_selectors = {
        1: {
            'selections': [(1, _('Fifteen minutes water consumption')),
                           (7, _('Hourly water consumption')),
                           (6, _('Raw measurements')),],
            'title': _('High resolution data'),
            'default': 1
        },
        2: {
            'selections': [(2, _('Daily water consumption')),
                           (3, _('Daily water consumption per capita')),],
            'title': _('Daily data'),
            'default': 2
        },
        4: {
            'selections': [(4, _('Monthly water consumption')),
                           # (8, 'Monthly water cost'),
                           (5, _('Monthly water consumption per capita')),],
            'title': _('Monthly data'),
            'default': 8
        },
        10: {
            'selections': [(10, _('Fifteen minutes energy consumption')),
                           (13, _('Hourly energy consumption'))],
            'title': _('High resolution data'),
            'default': 10
        },
        11: {
            'selections': [(11, _('Daily energy consumption')),
                           (15, _('Daily energy consumption per capita'))],
            'title': _('Daily data'),
            'default': 11
        },
        12: {
            'selections': [(12, _('Monthly energy consumption')),
                           # (16, 'Monthly energy cost'),
                           (17, _('Monthly energy consumption per capita'))],
            'title': _('Monthly data'),
            'default': 12
        },
    }
    variables = [
        {
            'id': 1, 'chart_id': 1, 'name': 'var_name',
            'timeseries_id': ts_fifteen.id,
            'is_bar': True, 'bar_width': 7*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 2, 'chart_id': 2, 'name': 'var_name',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 3, 'chart_id': 4, 'name': 'var_name',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1,
        },
        {
            'id': 4, 'chart_id': 6, 'name': 'var_name',
            'timeseries_id': ts_raw.id,
            'is_bar': False,
            'factor': 1.000,
        },
        {
            'id': 5, 'chart_id': 3, 'name': 'Household',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000/nocc,
        },
        {
            'id': 6, 'chart_id': 3, 'name': 'DMA',
            'timeseries_id': ts_dma_daily_pc.id,
            'factor': 1000.000,
        },
        {
            'id': 7, 'chart_id': 5, 'name': 'Household',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000/nocc,
        },
        {
            'id': 8, 'chart_id': 5, 'name': 'DMA',
            'timeseries_id': ts_dma_monthly_pc.id,
            'factor': 1.000,
        },
        {
            'id': 9, 'chart_id': 7, 'name': 'var_name',
            'timeseries_id': ts_hourly.id,
            'is_bar': True, 'bar_width': 30*60*1000,
            'factor': 1000.000,
        },
        # {
        #     'id': 10, 'chart_id': 8, 'name': 'var_name',
        #     'timeseries_id': ts_cost.id,
        #     'is_bar': True, 'bar_width': 14*24*60*60*1000,
        #     'factor': 1,
        # },
    ]
    # Energy Variables added by Chris Pantazis. These are needed
    # for the charts.js (js=javascript and not json)
    variables_nrg = []
    if has_energy:
        variables_nrg = [
            {
                'id': 11, 'chart_id': 10, 'name': 'energy',
                'timeseries_id': ts_fifteen_nrg.id,
                'is_bar': True, 'bar_width': 7*60*1000,
                'factor': 1000.000,
            },
            {
                'id': 12, 'chart_id': 11, 'name': 'energy',
                'timeseries_id': ts_daily_nrg.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1000.000,
            },
            {
                'id': 13, 'chart_id': 12, 'name': 'energy',
                # 'timeseries_id': ts_cost_nrg.id,
                # 'is_bar': True, 'bar_width': 14*24*60*60*1000,
                # 'factor': 1,
            },
            {
                'id': 14, 'chart_id': 13, 'name': 'energy',
                'timeseries_id': ts_hourly_nrg.id,
                'is_bar': True, 'bar_width': 30*60*1000,
                'factor': 1000.000,
            },
            {
                'id': 15, 'chart_id': 15, 'name': 'energy',
                'timeseries_id': ts_daily_nrg.id,
                'is_bar': True, 'bar_width': 11*60*60*1000,
                'factor': 1000.000/nocc,
            },
            {
                'id': 16, 'chart_id': 16, 'name': 'energy',
                # 'timeseries_id': ts_cost_nrg.id,
                # 'is_bar': True, 'bar_width': 14*24*60*60*1000,
                # 'factor': 1,
            },
            {
                'id': 17, 'chart_id': 17, 'name': 'energy',
                'timeseries_id': ts_monthly_nrg.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': 1.000/nocc,
            },
            {
                'id': 18, 'chart_id': 18, 'name': 'energy',
                'timeseries_id': ts_monthly_nrg.id,
                'is_bar': True, 'bar_width': 14*24*60*60*1000,
                'factor': 1.000,
            },
        ]
    pies = {
        1: {'timeseries_id': ts_hourly.id,
            'period_unit': 'hour',
            'period_from': 1,
            'period_to': 4,
            'default_period': 'Nightly consumption 1:00-04:00',
            'alternate_period': 'Daily consumption 04:01-24:59'},
        2: {'timeseries_id': ts_monthly.id,
            'period_unit': 'month',
            'period_from': 5,
            'period_to': 9,
            'default_period': 'Summer consumption (May-September)',
            'alternate_period': 'Winter consumption (October-April)'}
    }
    if has_energy:
        pies.update({
            3: {'timeseries_id': ts_hourly_nrg.id,
                'period_unit': 'hour',
                'period_from': 1,
                'period_to': 4,
                'default_period': 'Nightly consumption 1:00-04:00',
                'alternate_period': 'Daily consumption 04:01-24:59'},
            4: {'timeseries_id': ts_monthly_nrg.id,
                'period_unit': 'month',
                'period_from': 5,
                'period_to': 9,
                'default_period': 'Summer consumption (May-September)',
                'alternate_period': 'Winter consumption (October-April)'}
        })

    js_data = {
            'timeseries_data_url': '/timeseries/data/',#reverse('timeseries_data'), commented by Adeel and replace with Static URL
            'periods_stats_url': '/ajax/period_stats/',#reverse('periods_stats'), commented by Adeel and replace with Static URL
            'charts': charts,
            'charts_nrg': charts_nrg,
            'variables_nrg': variables_nrg,
            'variables': variables,
            'pies': pies
    }
    js_data = simplejson.dumps(js_data)
    form = HouseholdForm(instance=household)
    for field in form.fields:
        form.fields[field].required = False
        form.fields[field].widget.attrs['disabled'] = 'disabled'
        form.fields[field].help_text=u''
    # overview_nrg added by Chris Pantazis to show
    # energy data on dashboard
    if has_energy:
        overview_nrg = statistics_on_daily(ts_daily_nrg, nocc)
    else:
        overview_nrg = None
    return {
        'household': household,
        'charts': charts,
        'charts_nrg': charts_nrg,
        'form': form,
        'js_data': js_data,
        'chart_selectors': chart_selectors,
        'overview': statistics_on_daily(ts_daily, nocc),
        'overview_nrg': overview_nrg,
        'has_energy': has_energy,
    }


'''
Following methods is the copy of def dma_view(request, dma_id) except this method return values not to template.
'''
@login_required
def dmas_view(request, dma_id):
    user = request.user
    if not (user.is_staff or user.is_superuser):
        request.notifications.error(_("Permission denied"))
        return HttpResponseRedirect(reverse('index'))
    try:
        dma = DMA.objects.get(pk=dma_id)
    except DMA.DoesNotExist:
        raise Http404('DMA does not exist')

    ts_daily = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            ~Q(name__icontains='capita'))[0]
    ts_monthly = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            ~Q(name__icontains='capita'))[0]
    ts_daily_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_DAILY) &
            Q(name__icontains='capita'))[0]
    ts_monthly_pc = dma.timeseries.filter(Q(time_step__id=TSTEP_MONTHLY) &
            Q(name__icontains='capita'))[0]
    charts = [
        {
            'id': 1,
            'name': _('Daily water consumption (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_daily.id,
            'span_options': [_('year'), _('month'), _('week')],
            'initial_display': True,
        },
        {
            'id': 2,
            'name': _('Water consumption per month, up to a year period (m<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_monthly.id,
            'span_options': [],
            'initial_display': True,
        },
        {
            'id': 3,
            'name': _('Daily water consumption per capita (litres)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'week', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_daily_pc.id,
            'span_options': [_('year'), _('month'), _('week')],
            'initial_display': True,
        },
        {
            'id': 4,
            'name': _('Water consumption per month, up to a year period, per capita (<sup>3</sup>)'),
            'display_min': True, 'display_max': True, 'display_avg': True,
            'display_sum': True, 'time_span': 'year', 'is_vector': False,
            'has_stats': True, 'can_zoom': True, 'has_info_box': True,
            'display_lastvalue': True,
            'main_timeseries_id': ts_monthly_pc.id,
            'span_options': [],
            'initial_display': True,
        },
    ]
    variables = [
        {
            'id': 1, 'chart_id': 1, 'name': 'var_name',
            'timeseries_id': ts_daily.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1.000,
        },
        {
            'id': 2, 'chart_id': 2, 'name': 'var_name',
            'timeseries_id': ts_monthly.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000,
        },
        {
            'id': 3, 'chart_id': 3, 'name': 'var_name',
            'timeseries_id': ts_daily_pc.id,
            'is_bar': True, 'bar_width': 11*60*60*1000,
            'factor': 1000.000,
        },
        {
            'id': 4, 'chart_id': 4, 'name': 'var_name',
            'timeseries_id': ts_monthly_pc.id,
            'is_bar': True, 'bar_width': 14*24*60*60*1000,
            'factor': 1.000,
        },
    ]
    js_data = {
            'timeseries_data_url': reverse('timeseries_data'),
            'charts': charts,
            'variables': variables
    }
    js_data = simplejson.dumps(js_data)
    return  {'dma': dma,
             'charts': charts,
             'js_data': js_data}

from django.views.generic.base import TemplateView
#TemplateView class for agent based modelling page only available to superuser
class policy(TemplateView):
    template_name = "policy.html"

    def get(self,request,**kwargs):
        return self.render_to_response({})
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''End of Adeel changes''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('login'))
