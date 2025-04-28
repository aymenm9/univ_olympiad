from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('hospital','Hospital'),('DSP','DSP'),('APC','APC'),('admin','admin')], default='hospital')



from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=User)
def hash_password(sender, instance, **kwargs):
    if instance.password:
        instance.password = make_password(instance.password)