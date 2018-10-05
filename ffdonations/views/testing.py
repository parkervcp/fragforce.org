from django.shortcuts import render, Http404
from django.http import JsonResponse
from ..tasks import *
from django.db.models import Q, Avg, Max, Min, Sum
from django.views.decorators.cache import cache_page
from django.conf import settings
from functools import wraps


def _onlydebug(f):
    """ Decorator: Only run the view if we're in debug mode """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if not settings.DEBUG:
            raise Http404("DEBUG=False")

        return f(*args, **kwargs)

    return wrapped


@_onlydebug
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
