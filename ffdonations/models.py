from django.db import models
from django.db.models import Q
import uuid
from django.contrib.postgres.fields import JSONField
import datetime


class EventModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    tracked = models.BooleanField(default=False, verbose_name="Is Tracked")
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.BigIntegerField(primary_key=True, editable=False, verbose_name="Event ID", null=False)


class TeamModel(models.Model):
    """ All teams """
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    tracked = models.BooleanField(default=False, verbose_name="Is Tracked")
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.BigIntegerField(primary_key=True, editable=False, verbose_name="Team ID", null=False)
    name = models.CharField(max_length=8192, null=False, verbose_name="Team Name")
    # Info
    created = models.DateTimeField(verbose_name="Created At", null=True)
    fundraisingGoal = models.FloatField(verbose_name="Fundraising Goal", null=True)
    numDonations = models.BigIntegerField(verbose_name="Donation Count", null=True)
    sumDonations = models.FloatField(verbose_name="Donations Total", null=True)
    # Related
    event = models.ForeignKey(EventModel, null=True, default=None, verbose_name="Event", on_delete=models.DO_NOTHING)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)


class ParticipantModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    tracked = models.BooleanField(default=False, verbose_name="Is Tracked")
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.BigIntegerField(primary_key=True, editable=False, verbose_name="Participant ID", null=False)
    displayName = models.CharField(max_length=8192, verbose_name="Participant Name", null=True)
    # Info
    created = models.DateTimeField(verbose_name="Created At", null=True)
    avatarImage = models.URLField(verbose_name="Avatar Image", null=True, max_length=8192)
    campaignDate = models.DateTimeField(null=True, verbose_name="Campaign Date")
    campaignName = models.CharField(max_length=8192, null=True, verbose_name="Campaign Name")
    fundraisingGoal = models.FloatField(verbose_name="Fundraising Goal", null=True)
    numDonations = models.BigIntegerField(verbose_name="Donation Count", null=True)
    sumDonations = models.FloatField(verbose_name="Donations Total", null=True)
    sumPledges = models.FloatField(verbose_name="Pledges Total", null=True)
    isTeamCaptain = models.NullBooleanField(verbose_name="Is Team Captain", default=False, null=True)
    # Related
    event = models.ForeignKey(EventModel, null=True, default=None, verbose_name="Event", on_delete=models.DO_NOTHING)
    team = models.ForeignKey(TeamModel, null=True, default=None, verbose_name="Team", on_delete=models.DO_NOTHING)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)


class DonationModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.CharField(primary_key=True, max_length=1024, editable=False, verbose_name="Donation ID", null=False)
    message = models.CharField(max_length=1024 * 1024, verbose_name="Message", default='', null=True)
    amount = models.FloatField(null=True, default=0, verbose_name="Donation Amount")
    created = models.DateTimeField(verbose_name="Created At", null=False, default=datetime.datetime.utcnow)
    displayName = models.CharField(max_length=8192, verbose_name="Donor Name", null=True)
    avatarImage = models.URLField(verbose_name="Avatar Image", null=True, max_length=8192)

    # Related
    participant = models.ForeignKey(ParticipantModel, null=True, default=None, verbose_name="Participant",
                                    on_delete=models.DO_NOTHING)
    team = models.ForeignKey(TeamModel, null=True, default=None, verbose_name="Team", on_delete=models.DO_NOTHING)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)

    @classmethod
    def tracked_q(cls):
        """ Get a Q that filters Donations down to only tracked ones """
        return Q(team__tracked=True) | Q(participant__tracked=True)
