from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import *


@require_POST
def start(request):
    skey = request.POST['name']
    key = get_object_or_404(Key, key=skey)
    if not key.active:
        return HttpResponseForbidden("inactive key")
    # if key.is_live:
    # What to do if already live?

    key.is_live = True
    key.save()

    stream = Stream(key=key, owner=key.owner, is_live=True, started=timezone.now(), ended=None)
    stream.save()

    # Change key to GUID
    return HttpResponseRedirect(key.name + "__" + stream.guid)


@require_POST
def stop(request):
    skey = request.POST['name']
    key = get_object_or_404(Key, key=skey)
    key.is_live = False
    key.save()
    # End them all, just in case
    for stream in key.stream_set.filter(is_live=True, ended=None).all():
        stream.ended = timezone.now()
        stream.is_live = False
        stream.save()

    return HttpResponse("OK")
