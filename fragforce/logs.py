import logging
import logging.config
import os
import json
import logzio.handler

COPY_FROM_ENV = set([
    'DEBUG',
    'EXTRALIFE_TEAMID',
    'FILE_UPLOADS',
    'HEROKU_APP_ID',
    'HEROKU_APP_NAME',
    'HEROKU_DYNO_ID',
    'HEROKU_RELEASE_CREATED_AT',
    'HEROKU_RELEASE_VERSION',
    'HEROKU_SLUG_COMMIT',
    'HEROKU_SLUG_DESCRIPTION',
])

DEBUG = bool(os.environ.get('DEBUG', 'False').lower() == 'true')
LOGZIO_API_KEY = os.environ.get('LOGZIO_API_KEY', None)

##### Loggers #####
root_logger = logging.getLogger()
if DEBUG:
    root_logger.setLevel(logging.DEBUG)
else:
    root_logger.setLevel(logging.INFO)

urllib3_conn_logger = root_logger.getChild('urllib3')
urllib3_conn_logger.setLevel(logging.INFO)

##### Formatters #####
fmt_basic = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fmt_verbose = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')

# Any K:V pairs that should be included in all log lines
fixed_info = dict(
    appCode='fragforce.org',
)

# Add env var into fixed_info
for env_name in COPY_FROM_ENV:
    fixed_info[env_name] = os.environ.get(env_name, None)

fmt_logzio = logging.Formatter(json.dumps(fixed_info))

##### Handlers #####
# Console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(fmt_basic)
root_logger.addHandler(console)
root_logger.info("Console logging enabled")

if os.getenv('LOGZIO_API_KEY', None):
    logz = logzio.handler.LogzioHandler(
        token=os.getenv('LOGZIO_API_KEY', None),
        debug=False,  # Don't need to debug the logger itself
        url='https://listener.logz.io:8071',  # Is the default but let's set to ensure it's always https
    )
    logz.setLevel(3)
    logz.setFormatter(fmt_logzio)
    root_logger.addHandler(logz)
    root_logger.info("logz.io logging enabled")
else:
    root_logger.info("logz.io logging disabled")

