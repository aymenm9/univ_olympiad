from django.contrib import admin
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate, DeathCertificateUpdateRequest, BirthCertificateUpdateRequest, BurialPermit
# Register your models here.

admin.site.register(BirthRecord)
admin.site.register(DeathRecord)
admin.site.register(BirthCertificate)
admin.site.register(DeathCertificate)
admin.site.register(BirthCertificateUpdateRequest)
admin.site.register(DeathCertificateUpdateRequest)
admin.site.register(BurialPermit)
