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


def calc_costs(request, username):
    pass
