from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn

import config
import database

sched = BlockingScheduler()
high = Queue('high', connection=conn)
q = Queue('default', connection=conn)
low = Queue('low', connection=conn)

@sched.scheduled_job('interval', minutes=1)
def update_team():
    result = q.enqueue(database.update_team)

database.create_tables()
