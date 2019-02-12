from django.shortcuts import render, Http404
from django.http import JsonResponse
from ..tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
from django.views.decorators.cache import cache_page
from django.conf import settings


@cache_page(settings.VIEW_DONATIONS_CACHE)
def v_donations(request):
    orderByVar = request.GET['orderBy']
    if orderByVar is None
        orderByVar = 'id'
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.all().order_by(orderByVar).values()],
        safe=False,
    )


@cache_page(settings.VIEW_DONATIONS_CACHE)
def v_tracked_donations(request):
    orderByVar = request.GET['orderBy']
    if orderByVar is None
        orderByVar = 'id'
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.filter(DonationModel.tracked_q()).order_by(orderByVar).values()],
        safe=False,
    )
