import datetime

from django import template
from django.utils.timezone import localtime, now
from django.utils.timesince import timesince

register = template.Library()


def _coerce_date(value):
    if not value:
        return None

    if isinstance(value, datetime.datetime):
        return localtime(value).date()
    if isinstance(value, datetime.date):
        return value
    return None


@register.filter
def human_date(value):
    """
    Returns 'Today' if the date is today, else timesince.
    Works with date or datetime objects.
    """
    value_date = _coerce_date(value)
    if value_date is None:
        return str(value)

    today = localtime(now()).date()

    if value_date == today:
        return "Today"
    return timesince(value_date) + " ago"


@register.filter
def is_today(value):
    """Return True when the value is today, otherwise False."""
    value_date = _coerce_date(value)
    if value_date is None:
        return False

    return value_date == localtime(now()).date()


@register.filter
def days_since(value):
    """Return a human-friendly relative label for a date."""
    value_date = _coerce_date(value)
    if value_date is None:
        return ""

    today = localtime(now()).date()
    delta_days = (value_date - today).days

    if delta_days == 0:
        return "Today"
    if delta_days == -1:
        return "Yesterday"
    if delta_days == 1:
        return "Tomorrow"
    if delta_days < 0:
        if abs(delta_days) < 7:
            return f"{abs(delta_days)} days"
        if abs(delta_days) < 31:
            return "last week"
        if abs(delta_days) < 365:
            return "last month"
        return "last year"
    if delta_days < 7:
        return f"in {delta_days} days"
    return "next week"
