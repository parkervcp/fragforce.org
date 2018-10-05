from django.shortcuts import render, Http404
from django.http import JsonResponse
from .models import *
from .tasks import *


def testView(request):
    if not settings.DEBUG:
        raise Http404("Not in debug")
    ret = [
        update_donations_existing.delay(),
        update_participants.delay(),
        update_teams.delay(),
    ]

    return JsonResponse([repr(r) for r in ret], safe=False)


def teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.all().order_by('id').values()],
        safe=False,
    )


def tracked_teams(request):
    update_teams_if_needed.delay()
    return JsonResponse(
        [d for d in TeamModel.objects.filter(tracked=True).order_by('id').values()],
        safe=False,
    )


def participants(request):
    update_participants_if_needed.delay()
    return JsonResponse(
        [d for d in ParticipantModel.objects.all().order_by('id').values()],
        safe=False,
    )


def tracked_participants(request):
    update_participants_if_needed.delay()
    return JsonResponse(
        [d for d in ParticipantModel.objects.filter(tracked=True).order_by('id').values()],
        safe=False,
    )


def donations(request):
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.all().order_by('id').values()],
        safe=False,
    )


def tracked_donations(request):
    # FIXME: Limit to only fragforce donations!
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.all().order_by('id').values()],
        safe=False,
    )
