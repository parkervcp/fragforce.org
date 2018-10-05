from django.shortcuts import render, Http404
from django.http import JsonResponse
from .models import *
from .tasks import *
from django.db.models import Q, Avg, Max, Min, Sum


def testView(request):
    if not settings.DEBUG:
        raise Http404("Not in debug")
    ret = [
        # update_donations_existing.delay(),
        # update_participants.delay(),
        # update_teams.delay(),
    ]

    for team in TeamModel.objects.filter(tracked=True).all():
        ret.append(update_donations_if_needed_team.delay(team.id))

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
    update_donations_if_needed.delay()
    return JsonResponse(
        [d for d in DonationModel.objects.filter(DonationModel.tracked_q()).order_by('id').values()],
        safe=False,
    )


def tracked_donations_stats(request):
    update_donations_if_needed.delay()
    baseq = DonationModel.objects.filter(DonationModel.tracked_q()).order_by('id')
    ret = {
        'numDonations': baseq.count(),
        'sumDonations': baseq.aggergate(Sum('amount')).values()[0],
        'avgDonations': DonationModel.objects.aggergate(Avg('amount', filter=DonationModel.tracked_q())).values()[0],
        'minDonations': DonationModel.objects.aggergate(Min('amount', filter=DonationModel.tracked_q())).values()[0],
        'maxDonations': DonationModel.objects.aggergate(Max('amount', filter=DonationModel.tracked_q())).values()[0],
        'participants': baseq.distinct('participant').count(),
        'participants-with-donations': baseq.filter(participant__numDonations__gte=1).distinct('participant').count(),
        'teams': baseq.distinct('team').count(),
        'teams-with-donations': baseq.filter(team__numDonations__gte=1).distinct('team').count(),
    }
    return JsonResponse(ret)
