from .helpers import *
from ...models import *
from celery import shared_task


@shared_task(bind=True)
def update_campaigns(self):
    tf = get_tiltify()
    count = 0
    for c in tf.f_campaigns():
        try:
            o = CampaignTiltifyModel.objects.get(id=c.id)
        except CampaignTiltifyModel.DoesNotExist as e:
            n = {}
            for k in c.FIELDS_NORM:
                n[k] = getattr(c, k, None)

            o = CampaignTiltifyModel(**n)
            o.save()
            count += 1
    return count
