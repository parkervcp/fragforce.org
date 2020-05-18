from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
    # Handle loopback for ffmpeg
    if "__" in request.POST['name']:
        kname, sname = request.POST['name'].split("__")
        key = get_object_or_404(Key, name=kname)
        stream = key.stream_set.filter(guid=sname).get()
        return HttpResponseRedirect(key.name + "__" + str(stream.guid))

    if not request.GET.get('key', None):
        return HttpResponseForbidden("bad key")

    pullKey = get_object_or_404(Key, id=request.GET['key'])
    streamKey = get_object_or_404(Key, name=request.POST['name'])

    if not pullKey.pull:
        return HttpResponseForbidden("bad key")

    for stream in streamKey.stream_set.filter(is_live=True, ended=None).order_by("-started"):
        return HttpResponseRedirect(streamKey.name + "__" + str(stream.guid))

    return HttpResponseForbidden("inactive stream")


def view(request, key=None):
    pullKey = get_object_or_404(Key, id=key)
    if not pullKey.pull:
        return HttpResponseForbidden("bad key")

    return render(request, 'ffstream/view.html', dict(
        pullKey=pullKey,
        streams=Stream.objects.filter(is_live=True).order_by("-created").all(),
    ))
