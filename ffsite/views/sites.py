from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from ffsfdc.models import *


@cache_page(settings.VIEW_SITE_SITE_CACHE)
def sites(request):
    """ Sites page """
    return render(request, 'ff/sites/index.html', {
        'sites': SiteAccount.objects.order_by('name').all(),
    })


@cache_page(settings.VIEW_SITE_SITE_CACHE)
def site(request, sfid):
    """ Sites page """
    return render(request, 'ff/sites/site.html', {
        'site': SiteAccount.objects.filter(sfid=sfid).first(),
    })
