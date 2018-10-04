from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .tasks import *


def testView(request):
    from extralifeapi.teams import Teams, Team
    import json
    t = Teams()
    ret = []
    for team in t.teams():
        ret.append(team)
    return JsonResponse(ret)


def teams(request):
    update_teams.delay().wait()
    return JsonResponse(TeamModel.objects.all())
