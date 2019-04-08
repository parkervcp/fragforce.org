from django.shortcuts import render, Http404
from django.http import JsonResponse
from ..tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
from django.views.decorators.cache import cache_page
from django.conf import settings


@cache_page(settings.VIEW_DONATIONS_CACHE)
def v_donations(request):
    orderByVar = request.GET.get('orderBy', 'id')
    filterByVar = request.GET.get('filterBy', 'none')
    recordCountVar = request.GET.get('recordCount', '0')
    recordCountInt = int(recordCountVar)
    update_donations_if_needed.delay()
    if recordCountInt < 1:
        listedDonos = DonationModel.objects.order_by(orderByVar)
    else:
        listedDonos = DonationModel.objects.order_by(orderByVar)[:recordCountInt]
    if filterByVar != 'none':
        listedDonos = listedDonos.filter( participant_id == filterByVar )
    return JsonResponse(
        [d for d in listedDonos.values()],
        safe=False,
    )


@cache_page(settings.VIEW_DONATIONS_CACHE)
def v_tracked_donations(request):
    orderByVar = request.GET.get('orderBy', 'id')
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.filter(DonationModel.tracked_q()).order_by(orderByVar).values()],
        safe=False,
    )
