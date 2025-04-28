from django.contrib import admin
from .models import User
# Register your models here.



# hash the user password befout regster

admin.site.register(User)