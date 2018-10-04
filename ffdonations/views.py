from django.shortcuts import render
from django.http import JsonResponse


def testView(request):
    from extralifeapi.teams import Teams, Team
    import json
    t = Teams()
    ret = []
    for team in t.teams():
        ret.append(team)
    return JsonResponse(ret)
