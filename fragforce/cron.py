""" Run periodically """
from fragforce import app, sched


### Put cron entries here

@sched.scheduled_job('interval', minutes=60)
def update_team():
    """ """
    from .extralife import team
    t = team(app.config['EXTRALIFE_TEAMID'])


@sched.scheduled_job('interval', minutes=60)
def update_participants():
    """ """
    from .extralife import participants
    p = participants(app.config['EXTRALIFE_TEAMID'])

# Do NOT sched.start() - Done in clock.py
