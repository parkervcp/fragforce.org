from django.conf import settings

from .redisdb import *

# Timers
r_timers = TimersDB(settings.REDIS_URL_TIMERS)
