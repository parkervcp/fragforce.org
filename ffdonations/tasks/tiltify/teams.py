from celery import shared_task
from django.conf import settings

from .campaigns import update_campaigns
from .helpers import *
from ...models import *


@shared_task(bind=True)
def update_teams(self):
    """ Update all configured Tiltify teams from API to DB """
    tf = get_tiltify()
    created = 0
    updated = 0
    # Use slugs to resolve
    for slug in settings.TILTIFY_TEAMS:
        team = tf.f_team(slug)

        try:
            o = TeamTiltifyModel.objects.get(id=team.parsed['id'])

            n = {}
            for k in team.FIELDS_NORM:
                setattr(o, k, team.parsed.get(k, None))

            o.raw = team.data
            o.subtype = team.__class__.__name__

            o.save()
            updated += 1
        except TeamTiltifyModel.DoesNotExist as e:
            n = {}
            for k in team.FIELDS_NORM:
                n[k] = team.parsed.get(k, None)

            o = TeamTiltifyModel(
                raw=team.data,
                subtype=team.__class__.__name__,
                **n,
            )
            o.save()
            created += 1
        # Update the campaign in TF_CAMP_UPDATE_WAIT seconds
        update_campaigns.apply_async(kwargs=dict(team_id=team.parsed['id']), countdown=settings.TF_CAMP_UPDATE_WAIT)
    return created, updated
