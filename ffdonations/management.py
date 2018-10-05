# Block out CacheKeyWarnigns about cache key len
# https://docs.djangoproject.com/en/2.1/topics/cache/#cache-key-warnings
import warnings

from django.core.cache import CacheKeyWarning

warnings.simplefilter("ignore", CacheKeyWarning)
