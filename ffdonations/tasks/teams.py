from __future__ import absolute_import, unicode_literals
from celery import shared_task
from extralifeapi.teams import Team, Teams
from ..models import *
from django.conf import settings
import datetime


@shared_task(bind=True)
def update_teams_if_needed(self):
    """ Update the team list if required """

    def doupdate():
        return update_teams()

    minc = datetime.datetime.now() - settings.EL_TEAM_UPDATE_FREQUENCY_MIN
    maxc = datetime.datetime.now() - settings.EL_TEAM_UPDATE_FREQUENCY_MAX

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
    t = Teams()
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
        tm.save()
        ret.append(tm.guid)
    return ret
