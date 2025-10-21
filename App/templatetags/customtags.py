from django import template
from django.utils.timezone import localtime, now
from django.utils.timesince import timesince
import datetime

register = template.Library()

@register.filter
def human_date(value):
    """
    Returns 'Today' if the date is today, else timesince.
    Works with date or datetime objects.
    """
    if not value:
        return ""
    
    # convert datetime to date if necessary
    if isinstance(value, datetime.datetime):
        value_date = localtime(value).date()
    elif isinstance(value, datetime.date):
        value_date = value
    else:
        return str(value)
    
    today = localtime(now()).date()
    
    if value_date == today:
        return "Today"
    else:
        return timesince(value_date) + " ago"
