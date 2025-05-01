from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('hospital','Hospital'),('DSP','DSP'),('APC','APC'),('admin','admin')], default='hospital')



from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=User)
def hash_password(sender, instance, **kwargs):
    if instance.password:
        instance.password = make_password(instance.password)


class ChatHistory(models.Model):
    user = models.OneToOneField( 'users.User', on_delete=models.CASCADE, related_name='chat_history')
    msg = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user}, {self.msg}'