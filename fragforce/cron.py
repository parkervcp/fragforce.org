""" Run periodically """
from fragforce import app, sched, high, q, low


### Put cron entries here

@sched.scheduled_job('interval', minutes=2)
def _update_team():
    result = q.enqueue(update_team)


def update_team():
    """ """
    from .extralife import team
    t = team(app.config['EXTRALIFE_TEAMID'])


@sched.scheduled_job('interval', minutes=2)
def _update_participants():
    result = q.enqueue(update_participants)


def update_participants():
    """ """
    from .extralife import participants
    p = participants(app.config['EXTRALIFE_TEAMID'])

# Do NOT sched.start() - Done in clock.py
