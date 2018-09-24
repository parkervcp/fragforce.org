from django.shortcuts import render
from ffsfdc.models import *


def home(request):
    """ Home page """
    return render(request, 'ff/root/home.html', {})


def donate(request):
    """ How to donate page """
    from ..utils import random_contact
    return render(request, 'ff/root/donate.html', {
        'rnd_pct': random_contact(),
    })


def join(request):
    """ How to join ff page """
    return render(request, 'ff/root/join.html', {})


def contact(request):
    """ Contact page """
    return render(request, 'ff/root/contact.html', {})
