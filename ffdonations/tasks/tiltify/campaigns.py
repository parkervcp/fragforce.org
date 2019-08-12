import logging

from celery import shared_task

from .helpers import *
from ...models import *

log = logging.getLogger('ffdonations.tasks.tiltify.campaigns')


@shared_task(bind=True)
def update_campaigns(self, team_id):
    team = TeamTiltifyModel.objects.get(id=team_id)

    tf = get_tiltify()

    updated = 0
    created = 0
    for c in tf.f_team_campaigns(team.id):
        log.warning("Working on team-campaign %r", c.parsed.get('id', None), extra=dict(c=c.parsed))
        try:
            o = CampaignTiltifyModel.objects.get(id=int(c.parsed.get('id')))

            n = {}
            for k in c.FIELDS_NORM:
                setattr(o, k, c.parsed.get(k, None))

            o.team_id = team.id
            o.raw = c.data
            o.subtype = c.__class__.__name__

            o.save()
            updated += 1
        except CampaignTiltifyModel.DoesNotExist as e:
            n = {}
            for k in c.FIELDS_NORM:
                n[k] = c.parsed.get(k, None)

            o = CampaignTiltifyModel(
                raw=c.data,
                subtype=c.__class__.__name__,
                team=team,
                **n,
            )

            o.save()
            created += 1

    return created, updated
