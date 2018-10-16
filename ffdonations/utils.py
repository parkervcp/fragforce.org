# from .tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
#from django.conf import settings
from .models import *
from memoize import memoize


@memoize(timeout=120)
def el_num_donations():
    baseq = DonationModel.objects.filter(DonationModel.tracked_q())
    return baseq.count()


@memoize(timeout=120)
def el_donation_stats():
    baseq = DonationModel.objects.filter(DonationModel.tracked_q())
    return baseq.aggregate(
        sumDonations=Sum('amount'),
        avgDonation=Avg('amount'),
        minDonation=Min('amount'),
        maxDonation=Max('amount'),
    )
