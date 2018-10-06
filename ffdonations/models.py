from django.db import models
from django.db.models import Q
import uuid
from django.contrib.postgres.fields import JSONField
import datetime


## Extra-Life
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
    message = models.CharField(max_length=1024 * 1024, verbose_name="Message", default='', null=False)
    amount = models.FloatField(null=True, default=0, verbose_name="Donation Amount")
    created = models.DateTimeField(verbose_name="Created At", null=False, default=datetime.datetime.utcnow)
    displayName = models.CharField(max_length=8192, verbose_name="Donor Name", null=False, default='')
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


## Tiltify
class MediaTiltifyModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")
    id = models.BigAutoField(primary_key=True, verbose_name="ID")

    # Tiltify
    src = models.URLField(max_length=8192, null=False, verbose_name="Source URL")
    alt = models.CharField(max_length=8192, null=True, default='', verbose_name="Alternate Text")
    width = models.IntegerField(null=True, verbose_name="Width (px)")
    height = models.IntegerField(null=True, verbose_name="Height (px)")

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)

    # Type of result from lib
    subtype = models.CharField(max_length=255, null=False, default='MediaResult')


class CauseTiltifyModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Tilify
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)


class EventTiltifyModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Tilify
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)


class LiveStreamTiltifyModel(models.Model):
    pass

class TeamTiltifyModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Tilify
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Name", unique=True, null=False)
    slug = models.CharField(verbose_name="Slug", unique=True, null=False)
    url = models.CharField(verbose_name="URL", unique=True, null=False)
    avatar = models.ForeignKey(MediaTiltifyModel, verbose_name="Avatar", null=True, on_delete=models.DO_NOTHING)

    # On some
    bio = models.CharField(max_length=1024 * 1024, verbose_name="Bio")
    inviteOnly = models.NullBooleanField(verbose_name="Is Invite Only Team")
    disbanded = models.NullBooleanField(verbose_name="Is Disbanded")

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)

    # Type of result from lib
    subtype = models.CharField(max_length=255, null=False, default='TeamResult')


class UserTiltifyModel(models.Model):
    pass


class CampaignTiltifyModel(models.Model):
    # Ours
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="GUID", null=False)
    last_updated = models.DateTimeField(null=False, auto_now=True, verbose_name="Date Record Last Fetched")

    # Tilify
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=8192, verbose_name="Name", unique=True, null=False)
    slug = models.CharField(max_length=8192, verbose_name="Slug", unique=True, null=False)
    url = models.URLField(max_length=8192, verbose_name="URL", unique=True, null=False)
    startsAt = models.DateTimeField(null=True, verbose_name='Starts At')
    endsAt = models.DateTimeField(null=True, verbose_name='Ends At')
    description = models.CharField(max_length=8192, verbose_name="Description", unique=True, null=True)
    goal = models.FloatField(verbose_name="Goal Amount", null=True)
    fundraiserGoalAmount = models.FloatField(verbose_name="Fundraiser Goal Amount", null=True)
    originalGoalAmount = models.FloatField(verbose_name="Origional Goal Amount", null=True)
    amountRaised = models.FloatField(verbose_name="Amount Raised", null=True)
    supportingAmountRaised = models.FloatField(verbose_name="Supporting Amount Raised", null=True)
    totalAmountRaised = models.FloatField(verbose_name="Total Amount Raised", null=True)
    supportable = models.NullBooleanField(verbose_name="Is Supportable", null=True)
    status = models.CharField(max_length=8192, null=True, verbose_name="Status")
    startsOn = models.DateTimeField(null=True, verbose_name='Starts On')
    endsOn = models.DateTimeField(null=True, verbose_name='Ends On')

    thumbnail = models.ForeignKey(MediaTiltifyModel, verbose_name="Thumbnail", null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(UserTiltifyModel, verbose_name="user", null=True, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(TeamTiltifyModel, verbose_name="Team", null=True, on_delete=models.DO_NOTHING)
    livestream = models.ForeignKey(LiveStreamTiltifyModel, verbose_name="Live Stream", null=True,
                                   on_delete=models.DO_NOTHING)
    cause = models.ForeignKey(CauseTiltifyModel, verbose_name="Cause", null=True, on_delete=models.DO_NOTHING)
    avatar = models.ForeignKey(MediaTiltifyModel, verbose_name="Avatar", null=True, on_delete=models.DO_NOTHING)
    fundraisingEvent = models.ForeignKey(EventTiltifyModel, verbose_name="Fundrasing Event", null=True,
                                         on_delete=models.DO_NOTHING)

    # Extra
    raw = JSONField(verbose_name="Raw Data", null=True, default=dict)

    # Type of result from lib
    subtype = models.CharField(max_length=255, null=False, default='CampaignResult')


class DonationTiltifyModel(models.Model):
    pass
