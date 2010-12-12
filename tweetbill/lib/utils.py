import datetime
import dateutil

def parse_date(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    if isinstance(s, datetime.datetime):
        dt = s
    else:
        dt = dateutil.parser.parse(s)
    
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt
