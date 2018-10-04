from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .tasks import *


def testView(request):
    from extralifeapi.teams import Teams, Team
    ret = repr(update_teams.delay())

    return JsonResponse(ret, safe=False)


def teams(request):
    from django.forms.models import model_to_dict
    update_teams_if_needed.delay()
    return JsonResponse(
        [
            model_to_dict(
                t,
                fields=['id', 'guid'] + [field.name for field in TeamModel._meta.fields],
            )
            for t in TeamModel.objects.all()
        ],
        safe=False,
    )
