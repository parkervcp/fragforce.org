from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .tasks import *


def testView(request):
    ret = repr(update_teams.delay().get())

    return JsonResponse(ret, safe=False)


def teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.all().values()],
        safe=False,
    )


def tracked_teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.filter(tracked=True).values()],
        safe=False,
    )
