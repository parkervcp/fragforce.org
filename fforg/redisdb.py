""" Redis based caching and data storage """
import redis
from django.conf import settings
import hashlib


class RedisDB(object):
    def __init__(self, rurl):
        self.url = rurl
        self._conn = None

    @property
    def conn(self):
        # TODO: Add a ping in here
        if self._conn is None:
            self._conn = redis.StrictRedis.from_url(self.url)
        return self._conn

    def make_key(self, name, *args, **kwargs):
        arg_list = [name, ] + args + [f"{k}={v}" for k, v in kwargs.items()]
        return '_'.join(arg_list)

    def make_key_secure(self, name, *args, **kwargs):
        secret = settings.SECRET_KEY
        hash = hashlib.new('sha512')
        hash.update(secret)
        hash.update(self.make_key(name=name, *args, **kwargs))
        return str(hash)
