from django.contrib import admin
from .models import BirthRecord, DeathRecord
# Register your models here.

admin.site.register(BirthRecord)
admin.site.register(DeathRecord)
