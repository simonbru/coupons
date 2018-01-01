from datetime import datetime

from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def days_since(date):
    delta = now() - date
    return str(delta.days)
