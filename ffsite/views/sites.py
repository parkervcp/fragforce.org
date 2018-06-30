from django.shortcuts import render
from ffsfdc.models import *
from ffsite.models import *


def sites(request):
    """ Sites page """
    return render(request, 'ff/sites/index.html', {})


def site(request, sfid):
    """ Sites page """
    return render(request, 'ff/sites/site.html', {
        'site': SiteAccount.objects.filter(sfid=sfid).first(),
    })
