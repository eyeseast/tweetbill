from django.template import Library
from django.utils.dateformat import DateFormat

register = Library()

@register.filter('parsedate')
def parsedate(value, format=None):
    """
    Parses a date-like string into a Python datetime object,
    with an optional format argument, which follows Django's
    DateFormat, like the built-in date filter.
    """
    import dateutil.parser
    dt = dateutil.parser.parse(value)
    if format:
        return DateFormat(dt).format(format)
    return dt
