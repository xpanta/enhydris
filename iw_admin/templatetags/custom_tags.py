__author__ = 'Chris Pantazis'
from django import template
register = template.Library()


@register.filter(name='dict_get')
def dict_get(value, arg):
    try:
        v = value[arg]
        return v
    except KeyError:
        return ''


@register.filter(name='dict_get_num')
def dict_get_num(value, arg):
    try:
        v = value[arg]
        return v
    except KeyError:
        return 0

