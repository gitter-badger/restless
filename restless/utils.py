import datetime
import decimal
import traceback
try:
    from django.conf import settings
    from django.utils import timezone
except ImportError:
    settings = None
    timezone = None

try:
    import json
except ImportError:
    import simplejson as json


class MoreTypesJSONEncoder(json.JSONEncoder):
    """
    A JSON encoder that allows for more common Python data types.
    In addition to the defaults handled by ``json``, this also supports:
        * ``datetime.datetime``
        * ``datetime.date``
        * ``datetime.time``
        * ``decimal.Decimal``
    """
    def default(self, data):
        if isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
            return naive_datetime(data).isoformat()
        elif isinstance(data, decimal.Decimal):
            return str(data)
        else:
            return super(MoreTypesJSONEncoder, self).default(data)


def naive_datetime(value):
    if not settings or not timezone:
        return value

    if getattr(settings, "USE_TZ", False):
        default_tz = timezone.get_default_timezone()

        if isinstance(value, datetime.datetime) and timezone.is_aware(value):
            return timezone.make_naive(value, default_tz)
        elif isinstance(value, datetime.date):
            value = timezone.make_naive(
                datetime.datetime(value.year, value.month, value.day, tzinfo=timezone.UTC()),
                default_tz)

            return value.date()
        elif isinstance(value, datetime.time):
            value = timezone.make_naive(datetime.datetime(
                2001, 1, 1, hour=value.hour, minute=value.minute, second=value.second,
                microsecond=value.microsecond, tzinfo=timezone.UTC()), default_tz)

            return value.time()

    return value


def format_traceback(exc_info):
    stack = traceback.format_stack()
    stack = stack[:-2]
    stack.extend(traceback.format_tb(exc_info[2]))
    stack.extend(traceback.format_exception_only(exc_info[0], exc_info[1]))
    stack_str = "Traceback (most recent call last):\n"
    stack_str += "".join(stack)
    # Remove the last \n
    stack_str = stack_str[:-1]
    return stack_str