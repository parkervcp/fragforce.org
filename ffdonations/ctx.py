from .models import *
import datetime
from django.conf import settings
from .utils import *


def donations(request):
    """ Context processors for all ffdonations pages """
    return dict(
        # FIXME: Add custom caching here - use tasks to pregenerate so it doesn't slow down random pages
        el_donation_stats=el_donation_stats(),
        el_num_donations=el_num_donations(),
    )
