# from .tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
# from django.conf import settings
from .models import *
from memoize import memoize
from ffsfdc.models import *
from django.utils import timezone


# @memoize(timeout=120)
# def el_num_donations():
#     baseq = DonationModel.objects.filter(DonationModel.tracked_q())
#     return baseq.count()
#
#
# @memoize(timeout=120)
# def el_donation_stats():
#     baseq = DonationModel.objects.filter(DonationModel.tracked_q())
#     return baseq.aggregate(
#         sumDonations=Sum('amount'),
#         avgDonation=Avg('amount'),
#         minDonation=Min('amount'),
#         maxDonation=Max('amount'),
#     )

@memoize(timeout=120)
def event_name_maker(year=timezone.now().year):
    return 'Extra Life %d' % year


@memoize(timeout=120)
def el_teams(year=timezone.now().year):
    """ Returns a list of team IDs that we're tracking for the given year """
    yr = event_name_maker(year=year)
    ret = []
    for sa in SiteAccount.objects.filter(el_id__isnull=False).only('el_id').all():
        try:
            tm = TeamModel.objects.get(id=sa.el_id)
            if tm.event.name == yr:
                ret.append(tm.id)
        except TeamModel.DoesNotExist:
            pass
    return ret


@memoize(timeout=120)
def el_contact(year=timezone.now().year):
    """ Returns a list of participant IDs that we're tracking for the given year """
    yr = event_name_maker(year=year)
    ret = []
    for sa in Contact.objects.filter(extra_life_id__isnull=False).only('extra_life_id').all():
        try:
            tm = ParticipantModel.objects.get(id=sa.extra_life_id)
            if tm.event.name == yr:
                ret.append(tm.id)
        except ParticipantModel.DoesNotExist:
            pass
    return ret


@memoize(timeout=120)
def el_num_donations(year=timezone.now().year):
    """ For current year """
    tsum = TeamModel.objects.filter(id__in=el_teams(year=year)) \
        .aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    psum = ParticipantModel.objects.filter(Q(
        Q(team__tracked=False) | Q(id__in=el_teams(year=year))
    ), tracked=True) \
        .aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    return dict(
        countDonations=float(tsum + psum),
        countTeamDonations=float(tsum),
        countParticipantDonations=float(psum),
    )


@memoize(timeout=120)
def el_donation_stats(year=timezone.now().year):
    """ For current year """
    tsum = TeamModel.objects.filter(id__in=el_teams(year=year)) \
        .aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    psum = ParticipantModel.objects.filter(Q(
        Q(team__tracked=False) | Q(id__in=el_teams(year=year))
    ), tracked=True) \
        .aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    return dict(
        sumDonations=float(tsum + psum),
        sumteamDonations=float(tsum),
        sumparticipantDonations=float(psum),
    )
