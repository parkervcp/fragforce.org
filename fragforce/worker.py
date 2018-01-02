import logging,logging.config
import os
import redis
from rq import Worker, Queue, Connection
from .logs import root_logger

log = root_logger.getChild('fragforce.worker')
listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
log_api_key = os.environ.get('LOGZIO_API_KEY', None)

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    log.info("Building Redis connection")
    with Connection(conn):
        log.info("Building worker")
        worker = Worker(map(Queue, listen))
        log.info("Starting work")
        worker.work()
    log.info("All done")
