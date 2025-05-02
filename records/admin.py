from django.contrib import admin
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate
# Register your models here.

admin.site.register(BirthRecord)
admin.site.register(DeathRecord)
admin.site.register(BirthCertificate)
admin.site.register(DeathCertificate)
