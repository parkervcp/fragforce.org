""" Redis based caching and data storage """
import redis
from django.conf import settings
import hashlib
import time
from datetime import timedelta


class RedisDB(object):
    def __init__(self, rurl):
        self.url = rurl
        self._conn = None

    @property
    def db(self):
        # TODO: Add a ping in here
        if self._conn is None:
            self._conn = redis.StrictRedis.from_url(self.url)
        return self._conn

    def make_key(self, name, *args, **kwargs):
        kwsort = list(kwargs.items())
        kwsort.sort(key=lambda x: x[0])
        arg_list = [name, ] + args + [f"{k}={v}" for k, v in kwsort]
        return '_'.join(arg_list)

    def make_key_secure(self, name, *args, **kwargs):
        secret = settings.SECRET_KEY
        hash = hashlib.new('sha512')
        hash.update(secret)
        hash.update(self.make_key(name=name, *args, **kwargs))
        return str(hash)


class TimersDB(RedisDB):
    def time_until(self, key, delta=timedelta(seconds=1), now=time.time()):
        """ The amount of time between calls. Zero if not called before. """
        r = self.db.get(key)
        if r is None:
            self.db.set(key, str(now), ex=delta)
            return timedelta(seconds=0)
        r = float(r)
        expected = r + delta.total_seconds()
        diff = now - expected
        if diff <= 0:
            return timedelta(seconds=0)
        return timedelta(seconds=diff)
