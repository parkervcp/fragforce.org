import time
from fforg.rdbs import r_timers
from django.conf import settings


def el_request_sleeper(url, data, parsed, **kwargs):
    """ Ensure we don't make requests to EL too fast """
    host = parsed.hostname
    key_global = r_timers.make_key('el_request_sleeper')
    key_host = r_timers.make_key('', host=host)
    key_url = r_timers.make_key('el_request_sleeper', url=url)

    sleeps = dict(
        global_sleep=r_timers.time_until(key_global, settings.EL_REQUEST_MIN_TIME).total_seconds(),
        host_sleep=r_timers.time_until(key_host, settings.REQUEST_MIN_TIME_HOST).total_seconds(),
        url_sleep=r_timers.time_until(key_url, settings.EL_REQUEST_MIN_TIME_URL).total_seconds(),
    )

    srt = sleeps.items()
    srt.sort(key=lambda x: x[1], reverse=True)
    sleep_type, sleep_sec = srt[0]

    time.sleep(sleep_sec)
    return sleep_type
