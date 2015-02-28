__author__ = 'Chris Pantazis'
from django import template
from datetime import datetime, timedelta
register = template.Library()


@register.filter
def yesterday(value):
    return value - timedelta(days=1)



