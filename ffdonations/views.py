from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .tasks import *


def testView(request):
    ret = repr(update_teams.delay())

    return JsonResponse(ret, safe=False)


def teams(request):
    from django.forms.models import model_to_dict
    update_teams_if_needed.delay()
    return JsonResponse(
        TeamModel.objects.all().values(),
        safe=False,
    )
