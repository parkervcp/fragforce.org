import time
from fforg.rdbs import r_timers
from django.conf import settings


def el_request_sleeper(url, data, **kwargs):
    """ Ensure we don't make requests to EL too fast """
    min_sleep = settings.EL_REQUEST_MIN_TIME
    key_global = r_timers.make_key('el_request_sleeper')
    key_url = r_timers.make_key('el_request_sleeper', url=url)

    global_sleep = r_timers.time_until(key_global, min_sleep).total_seconds()
    url_sleep = r_timers.time_until(key_url, min_sleep).total_seconds()

    if global_sleep > url_sleep:
        time.sleep(global_sleep)
    else:
        time.sleep(url_sleep)
