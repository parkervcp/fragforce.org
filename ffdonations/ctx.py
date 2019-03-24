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
    ret['childsplay'] = 0  # Stubs for CP & Singapore
    ret['singapore'] = 0  # Stubs for CP & Singapore
    ret['sumDonations'] = ret['extralife'] + ret['childsplay'] + ret['singapore']
    ret['target'] = 200000
    ret['togo'] = ret['target'] - ret['sumDonations']
    return ret
