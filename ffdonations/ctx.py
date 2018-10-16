from .models import *
import datetime
from django.conf import settings
from .utils import *


def donations(request):
    """ Context processors for all ffdonations pages """
    return dict(
        el_donation_stats=el_donation_stats(),
    )