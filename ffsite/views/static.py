from django.shortcuts import render
from ffsfdc.models import *


def home(request):
    """ Home page """
    return render(request, 'ff/root/home.html', {})


def donate(request):
    """ How to donate page """
    return render(request, 'ff/root/donate.html', {
        'rnd_pct': Contact.object.filter(extra_life_id__isnull=False),
    })


def join(request):
    """ How to join ff page """
    return render(request, 'ff/root/join.html', {})


def contact(request):
    """ Contact page """
    return render(request, 'ff/root/contact.html', {})
