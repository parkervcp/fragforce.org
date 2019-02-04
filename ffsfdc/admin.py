from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hcmeta)
admin.site.register(SfEventLog)
admin.site.register(TriggerLog)
admin.site.register(TriggerLogArchive)
admin.site.register(SiteAccount)
admin.site.register(Contact)
admin.site.register(ELHistory)
admin.site.register(Event)
admin.site.register(EventParticipant)
