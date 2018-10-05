from __future__ import absolute_import, unicode_literals
from celery import shared_task
from extralifeapi.teams import Team, Teams
from ..models import *
from django.conf import settings
import datetime


def _make_team(*args, **kwargs):
    """ Make a safe team object """
    from ..helpers import el_request_sleeper
    kwargs.setdefault('request_sleeper', el_request_sleeper)
    return Teams(*args, **kwargs)


@shared_task(bind=True)
def update_teams_if_needed(self):
    """ Update the team db if required """

    def doupdate():
        return update_teams()

    if TeamModel.objects.all().count() <= 0:
        return doupdate()

    minc = datetime.datetime.utcnow() - settings.EL_TEAM_UPDATE_FREQUENCY_MIN
    maxc = datetime.datetime.utcnow() - settings.EL_TEAM_UPDATE_FREQUENCY_MAX

    bq = TeamModel.objects.filter(tracked=True)

    # Force an update if it's been more than EL_TEAM_UPDATE_FREQUENCY_MAX since last
    # update for any record
    if bq.filter(last_updated__lte=maxc).count() > 0:
        return doupdate()

    # Skip updating if it's been less than EL_TEAM_UPDATE_FREQUENCY_MIN since last update
    # for any record
    if bq.filter(last_updated__gte=minc).count() > 0:
        return None

    # Guess we'll do an update!
    return doupdate()


@shared_task(bind=True)
def update_teams(self, teams=None):
    """ Update data in the team model from online data.
    WARNING: Listing teams causes an api call per team given
    WARNING: If teams is None then will fetch a list of ALL teams - May make many requests
    """
    t = _make_team()
    ret = []
    if teams is None:
        tr = t.teams()
    else:
        tr = [t.team(teamID=tid) for tid in teams]
    for team in tr:
        if team.eventID:
            try:
                evt = EventModel.objects.get(id=team.eventID)
            except EventModel.DoesNotExist as e:
                evt = EventModel(tracked=False, id=team.eventID)
                evt.save()
        else:
            evt = None

        try:
            tm = TeamModel.objects.get(id=team.teamID)

        except TeamModel.DoesNotExist as e:
            tm = TeamModel(
                tracked=False,
                id=team.teamID,
            )
        tm.name = team.name
        tm.created = team.createdDateUTC
        tm.fundraisingGoal = team.fundraisingGoal
        tm.numDonations = team.numDonations
        tm.sumDonations = team.sumDonations
        tm.event = evt
        tm.raw = team.raw
        tm.save()
        ret.append(tm.guid)
    return ret
