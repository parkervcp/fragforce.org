from django.shortcuts import render, Http404
from django.http import JsonResponse
from ..tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
from django.views.decorators.cache import cache_page
from django.conf import settings


@cache_page(settings.VIEW_TEAMS_CACHE)
def teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.all().order_by('id').values()],
        safe=False,
    )


@cache_page(settings.VIEW_TEAMS_CACHE)
def tracked_teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.filter(tracked=True).order_by('id').values()],
        safe=False,
    )
