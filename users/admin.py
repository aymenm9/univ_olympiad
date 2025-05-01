from django.contrib import admin
from .models import UserInfo, Hospital, DSP, APC
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Hospital)
admin.site.register(DSP)
admin.site.register(APC)



