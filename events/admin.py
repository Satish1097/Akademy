from django.contrib import admin
from events.models import *

admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(SavedEvent)
admin.site.register(Registration)
admin.site.register(Certificate)
admin.site.register(CertificateIssue)


# Register your models here.
