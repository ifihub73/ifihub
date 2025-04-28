from django import template
from django.utils.timezone import now
from datetime import timedelta

register = template.Library()

@register.filter
def time_ago(value):
    """
    Human-readable time difference with future support.
    """
    if not value:
        return ""

    now_time = now()
    diff = value - now_time  # time into the future is positive
    seconds = int(diff.total_seconds())
    is_future = seconds > 0

    seconds = abs(seconds)
    minutes = seconds // 60
    hours = seconds // 3600
    days = abs(diff.days)

    if seconds < 60:
        return "just now"
    
    if minutes < 60:
        unit = f"{minutes} min{'s' if minutes != 1 else ''}"
    elif hours < 24:
        unit = f"{hours} hour{'s' if hours != 1 else ''}"
    elif days == 1:
        unit = "tomorrow" if is_future else "yesterday"
        return unit
    elif days < 7:
        unit = f"{days} day{'s' if days != 1 else ''}"
    elif days < 30:
        weeks = days // 7
        unit = f"{weeks} week{'s' if weeks != 1 else ''}"
    elif days < 365:
        months = days // 30
        unit = f"{months} month{'s' if months != 1 else ''}"
    else:
        years = days // 365
        unit = f"{years} year{'s' if years != 1 else ''}"

    return f"in {unit}" if is_future else f"{unit} ago"
