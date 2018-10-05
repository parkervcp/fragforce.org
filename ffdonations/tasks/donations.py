from __future__ import absolute_import, unicode_literals
from celery import shared_task
from extralifeapi.donors import Donations, Donation
from ..models import *
from django.conf import settings
import datetime


def _make_d(*args, **kwargs):
    """ Make a safe Donations object """
    from ..helpers import el_request_sleeper
    kwargs.setdefault('request_sleeper', el_request_sleeper)
    return Donations(*args, **kwargs)


@shared_task(bind=True)
def update_donations_if_needed(self):
    """ Update the donations db if required - This updates all EXISTING donations!
    May not capture ones if we don't have donations for that team/participant already.
    See update_donations_if_needed_team and update_donations_if_needed_participant.
    """

    def doupdate():
        return update_donations_existing()

    minc = datetime.datetime.utcnow() - settings.EL_DON_UPDATE_FREQUENCY_MIN
    maxc = datetime.datetime.utcnow() - settings.EL_DON_UPDATE_FREQUENCY_MAX

    if DonationModel.objects.all().count() <= 0:
        return doupdate()

    bq = DonationModel.objects

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
def update_donations_existing(self):
    """ Update donations based on all existing participants and teams that are known based
    on the donations DB
    """
    teamIDs = set(DonationModel.objects.filter(team__isnull=False).values('team').distinct('team'))
    participantIDs = set(
        DonationModel.objects.filter(participant__isnull=False).values('participant').distinct('participant'))

    ret = []
    for teamID in teamIDs:
        ret.append(update_donations_if_needed_team.delay(teamID=teamID))
    for participantID in participantIDs:
        ret.append(update_donations_if_needed_participant.delay(participantID=participantID))
    return ret


@shared_task(bind=True)
def update_donations_if_needed_team(self, teamID):
    """ """
    d = _make_d()
    ret = []

    if teamID is None:
        return ret

    try:
        team = TeamModel.objects.get(id=teamID)
    except TeamModel.DoesNotExist as e:
        team = TeamModel(id=teamID, tracked=False)
        team.save()

    for donation in d.donations_for_team(teamID=teamID):
        # Get/create participant if it's set...
        if donation.participantID:
            try:
                participant = ParticipantModel.objects.get(id=donation.participantID)
            except ParticipantModel.DoesNotExist as e:
                participant = ParticipantModel(id=donation.participantID, tracked=False)
                participant.save()
        else:
            participant = None

        try:
            tm = DonationModel.objects.get(id=donation.donorID)
        except DonationModel.DoesNotExist as e:
            tm = DonationModel(id=donation.donorID)
        tm.team = team
        tm.participant = participant
        tm.raw = donation.raw
        tm.avatarImage = donation.avatarImageURL
        tm.displayName = donation.displayName
        tm.created = donation.createdDateUTC
        tm.amount = donation.amount
        tm.message = donation.message
        tm.save()


@shared_task(bind=True)
def update_donations_if_needed_participant(self, participantID):
    """ """
    d = _make_d()
    ret = []

    if participantID is None:
        return ret

    try:
        participant = ParticipantModel.objects.get(id=participantID)
    except ParticipantModel.DoesNotExist as e:
        participant = ParticipantModel(id=participantID, tracked=False)
        participant.save()

    for donation in d.donations_for_participants(participantID=participantID):
        # Get/create participant if it's set...
        if donation.teamID:
            try:
                team = TeamModel.objects.get(id=donation.teamID)
            except TeamModel.DoesNotExist as e:
                team = TeamModel(id=donation.teamID, tracked=False)
                team.save()
        else:
            team = None

        try:
            tm = DonationModel.objects.get(id=donation.donorID)
        except DonationModel.DoesNotExist as e:
            tm = DonationModel(id=donation.donorID)
        tm.team = team
        tm.participant = participant
        tm.raw = donation.raw
        tm.avatarImage = donation.avatarImageURL
        tm.displayName = donation.displayName
        tm.created = donation.createdDateUTC
        tm.amount = donation.amount
        tm.message = donation.message
        tm.save()
        ret.append(tm.guid)
    return ret
