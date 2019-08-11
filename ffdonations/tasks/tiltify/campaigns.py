from celery import shared_task

from .helpers import *
from ...models import *


@shared_task(bind=True)
def update_campaigns(self, team_id):
    team = TeamTiltifyModel.objects.get(id=team_id)

    tf = get_tiltify()

    updated = 0
    created = 0
    for c in tf.f_team_campaigns(team.id):
        try:
            o = CampaignTiltifyModel.objects.get(id=c.id)

            n = {}
            for k in c.FIELDS_NORM:
                setattr(o, k, getattr(c, k, None))

            o.team_id = team.id
            o.raw = c.data
            o.subtype = c.__class__.__name__

            o.save()
            updated += 1
        except CampaignTiltifyModel.DoesNotExist as e:
            n = {}
            for k in c.FIELDS_NORM:
                n[k] = getattr(c, k, None)

            o = CampaignTiltifyModel(
                raw=c.data,
                subtype=c.__class__.__name__,
                team_id=team.id,
                **n,
            )

            o.save()
            created += 1

    return created, updated
