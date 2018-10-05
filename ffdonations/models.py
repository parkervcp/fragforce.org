from django.db import models
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
    created = models.DateTimeField(verbose_name="Created At", null=False)
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
    displayName = models.CharField(max_length=8192, verbose_name="Participant Name", default='FIXME')
    # Info
    created = models.DateTimeField(verbose_name="Created At", null=False, default=datetime.datetime.utcnow)
    avatarImage = models.URLField(verbose_name="Avatar Image", null=True)
    campaignDate = models.DateTimeField(null=True, verbose_name="Campaign Date")
    campaignName = models.CharField(max_length=8192, null=True, verbose_name="Campaign Name")
    fundraisingGoal = models.FloatField(verbose_name="Fundraising Goal", null=True)
    numDonations = models.BigIntegerField(verbose_name="Donation Count", null=True)
    sumDonations = models.FloatField(verbose_name="Donations Total", null=True)
    isTeamCaptain = models.BooleanField(verbose_name="Is Team Captain", default=False, null=False)
    # Related
    event = models.ForeignKey(EventModel, null=True, default=None, verbose_name="Event", on_delete=models.DO_NOTHING)
    team = models.ForeignKey(TeamModel, null=True, default=None, verbose_name="Team", on_delete=models.DO_NOTHING)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)


class DonationModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    tracked = models.BooleanField(default=False, verbose_name="Is Tracked")
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.BigIntegerField(primary_key=True, editable=False, verbose_name="Donation ID", null=False)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)


class DonorModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    tracked = models.BooleanField(default=False, verbose_name="Is Tracked")
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Extra-Life
    id = models.BigIntegerField(primary_key=True, editable=False, verbose_name="Donor ID", null=False)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)
