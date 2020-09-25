from django.http import JsonResponse
from django.conf import settings
from django.db.models import Avg, Max, Min, Sum
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from ..tasks import *


@cache_page(settings.VIEW_DONATIONS_STATS_CACHE)
def v_tracked_donations_stats(request):
    update_donations_if_needed.delay()
    baseq = DonationModel.objects.filter(DonationModel.tracked_q())
    ret = baseq.aggregate(
        sumDonations=Sum('amount'),
        avgDonation=Avg('amount'),
        minDonation=Min('amount'),
        maxDonation=Max('amount'),
    )

    ret['numDonations'] = baseq.count()
    ret['participants-with-donations-synced'] = baseq.order_by('participant__id').distinct('participant__id').count()
    ret['participants-with-donations-actual'] = baseq.filter(participant__numDonations__gte=1).order_by(
        'participant__id').distinct('participant__id').count()
    ret['teams-with-donations-synced'] = baseq.order_by('team__id').distinct('team__id').count()
    ret['teams-with-donations-actual'] = baseq.filter(team__numDonations__gte=1).order_by('team__id').distinct(
        'team__id').count()

    ret['tracked-participants'] = ParticipantModel.objects.filter(tracked=True).count()
    ret['tracked-teams'] = TeamModel.objects.filter(tracked=True).count()

    return JsonResponse(ret)
