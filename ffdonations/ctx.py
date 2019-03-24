from .models import *
import datetime
from django.conf import settings
from .utils import *


def donations(request):
    """ Context processors for all ffdonations pages """
    ret = dict(
        # FIXME: Add custom caching here - use tasks to pregenerate so it doesn't slow down random pages
        el_donation_stats=el_donation_stats(),
        el_num_donations=el_num_donations(),
    )
    ret['extralife'] = ret['el_donation_stats']['sumDonations']
    ret['childsplay'] = settings.CHILDSPLAY_DONATIONS
    ret['singapore'] = settings.SINGAPORE_DONATIONS
    ret['sumDonations'] = ret['extralife'] + ret['childsplay'] + ret['singapore']
    ret['target'] = settings.TARGET_DONATIONS
    ret['togo'] = ret['target'] - ret['sumDonations']
    return ret
