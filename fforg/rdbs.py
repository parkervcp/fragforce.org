from .redisdb import RedisDB
from django.conf import settings

# Misc timers
r_timers = RedisDB(settings.REDIS_URL_TIMERS)
