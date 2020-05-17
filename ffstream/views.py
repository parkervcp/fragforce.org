from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *


@csrf_exempt
@require_POST
def start(request):
    skey = request.POST['name']
    key = get_object_or_404(Key, id=skey)
    if not key.active:
        return HttpResponseForbidden("inactive key")
    # if key.is_live:
    # What to do if already live?

    key.is_live = True
    key.save()

    stream = Stream(key=key, is_live=True, started=timezone.now(), ended=None)
    stream.save()

    # Change key to GUID
    return HttpResponseRedirect(key.name + "__" + str(stream.guid))


@csrf_exempt
@require_POST
def stop(request):
    skey = request.POST['name']
    key = get_object_or_404(Key, id=skey)
    key.is_live = False
    key.save()
    # End them all, just in case
    for stream in key.stream_set.filter(is_live=True, ended=None).all():
        stream.ended = timezone.now()
        stream.is_live = False
        stream.save()

    return HttpResponse("OK")


@csrf_exempt
@require_POST
def play(request):
    skey = request.POST['name']
    key = get_object_or_404(Key, id=skey)
    if not key.active:
        return HttpResponseForbidden("inactive key")

    for stream in key.stream_set.filter(is_live=True, ended=None).order_by("-started"):
        return HttpResponseRedirect(key.name + "__" + str(stream.guid))

    # Change key to GUID
    return HttpResponseForbidden("inactive stream")
