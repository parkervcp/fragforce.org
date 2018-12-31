# from .tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
# from django.conf import settings
from .models import *
from memoize import memoize


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
def el_num_donations():
    tsum = TeamModel.objects.filter(tracked=True).aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    psum = ParticipantModel.objects.filter(Q(Q(team__tracked=False) | Q(team__isnull=True)), tracked=True) \
        .aggregate(ttl=Sum('numDonations')).get('ttl', 0)
    return dict(
        countDonations=float(tsum + psum),
        countTeamDonations=float(tsum),
        countParticipantDonations=float(psum),
    )


@memoize(timeout=120)
def el_donation_stats():
    tsum = TeamModel.objects.filter(tracked=True).aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    psum = ParticipantModel.objects.filter(Q(Q(team__tracked=False) | Q(team__isnull=True)), tracked=True) \
        .aggregate(ttl=Sum('sumDonations')).get('ttl', 0)
    return dict(
        sumDonations=float(tsum + psum),
        sumteamDonations=float(tsum),
        sumparticipantDonations=float(psum),
    )
