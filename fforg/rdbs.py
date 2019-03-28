from .redisdb import *
from django.conf import settings

# Timers
r_timers = TimersDB(settings.REDIS_URL_TIMERS)
