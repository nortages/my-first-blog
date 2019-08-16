from datetime import datetime
from django import template

register = template.Library()


@register.filter
def is_today(dt):
  if isinstance(dt, datetime):
    return dt.date() == datetime.today().date()
  if isinstance(dt, date):
    return dt == datetime.today().date()

@register.filter
def is_thisYear(dt):
  return dt.year == datetime.now().year

@register.filter
def get(dict_obj, name):
	return dict_obj.get(name)
