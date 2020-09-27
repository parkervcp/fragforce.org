from ffsfdc.models import *
from random import randint

from django.db.models import Q, Max, Min

from ffsfdc.models import *


def random_contact():
    """ Returns a randomly selected Contact """
    # Limit all queries to these
    baseQ = Q(extra_life_id__isnull=False)
    info = Contact.objects.filter(baseQ).all().aggregate(Min('id'), Max('id'))
    pk = randint(info['id__min'], info['id__max'])
    r = Contact.objects.filter(baseQ).filter(pk=pk).first()
    if r:
        return r
    else:
        # Retry if the contact doesn't exist
        return random_contact()
