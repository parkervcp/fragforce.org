"""
Django settings for fforg project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
import django_heroku
from datetime import timedelta
import redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', 'True').lower() == 'true')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')
if SECRET_KEY == 'INSECURE':
    if DEBUG:
        import warnings

        warnings.warn('INSECURE SECRET_KEY!', RuntimeWarning)
    else:
        raise ValueError("SECRET_KEY env var must be defined when not in DEBUG=True")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'ffsite',
    'ffsfdc',
    'ffdonations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fforg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ffsite.ctx.common_org',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'fforg.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'hc': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db-hc.sqlite3'),
    },
}
DATABASE_ROUTERS = ["fforg.router.HCRouter", ]
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))
DATABASES['hc'].update(dj_database_url.config(conn_max_age=500, ssl_require=True, env="HC_RO_URL"))
try:
    DATABASES['hc']['OPTIONS']['options'] = '-c search_path=%s' % os.environ.get('HC_RO_SCHEMA', 'org')
except KeyError as e:
    pass

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Base URL - Needs DB ID added
REDIS_URL_BASE = os.environ.get('REDIS_URL', 'redis://localhost')
# Don't use DB 0 for anything
REDIS_URL_DEFAULT = REDIS_URL_BASE + "/0"
# Celery tasks
REDIS_URL_TASKS = REDIS_URL_BASE + "/1"
# Celery tombstones (aka results)
REDIS_URL_TOMBS = REDIS_URL_BASE + "/2"
# Misc timers
REDIS_URL_TIMERS = REDIS_URL_BASE + "/3"


CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ACKS_LATE = True
CELERY_BROKER_URL = REDIS_URL_TASKS
CELERY_RESULT_BACKEND = REDIS_URL_TOMBS

GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', None)
MAX_UPCOMING_EVENTS = int(os.environ.get('MAX_UPCOMING_EVENTS', 20))
MAX_PAST_EVENTS = int(os.environ.get('MAX_PAST_EVENTS', 20))
MAX_ALL_EVENTS = int(os.environ.get('MAX_ALL_EVENTS', 20))

# Min time between team updates - Only cares about tracked teams!
EL_TEAM_UPDATE_FREQUENCY_MIN = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_MIN', 30)))
# Max time between updates for any given team - Only cares about tracked teams!
EL_TEAM_UPDATE_FREQUENCY_MAX = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_MAX', 120)))
# How often to check for updates
EL_TEAM_UPDATE_FREQUENCY_CHECK = timedelta(minutes=int(os.environ.get('EL_TEAM_UPDATE_FREQUENCY_CHECK', 5)))

# Min time between EL REST requests
EL_REQUEST_MIN_TIME = timedelta(seconds=int(os.environ.get('EL_REQUEST_MIN_TIME_SECONDS', 15)))
# Min time between EL REST requests for any given URL
EL_REQUEST_MIN_TIME_URL = timedelta(seconds=int(os.environ.get('EL_REQUEST_MIN_TIME_URL_SECONDS', 120)))

# Second to last
CELERY_BEAT_SCHEDULE = {
    'update-all-teams': {
        'task': 'ffdonations.tasks.teams.update_teams_if_needed',
        'schedule': EL_TEAM_UPDATE_FREQUENCY_CHECK,
    },
}

# Activate Django-Heroku - Very last
django_heroku.settings(locals())
