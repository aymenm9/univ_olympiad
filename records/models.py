from django.db import models
from users.models import User
# Create your models here.


class BirthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('men','men'), ('female','female')], default='men')
    rh = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    nuber_of_birth = models.IntegerField(null=True)


class DeathRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    date_of_deth = models.DateField()
    sex = models.CharField(max_length=10, choices=[
        ('men','men'), ('female','female')], default='men')
    death_cause = models.CharField(max_length=10,null=True)
    age = models.IntegerField(default=0)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    nuber_of_birth = models.IntegerField(null=True)



from django.db.models.signals import pre_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

@receiver(pre_save, sender=BirthRecord)
def encrypt_data(sender, instance, **kwargs):
    load_dotenv()
    key = os.getenv('FERNET_KEY')
    fernet = Fernet(key)
    instance.first_name = fernet.encrypt(instance.first_name.encode()).decode()
    instance.last_name = fernet.encrypt(instance.last_name.encode()).decode()
    instance.father_name = fernet.encrypt(instance.father_name.encode()).decode()
    instance.mother_name = fernet.encrypt(instance.mother_name.encode()).decode()


@receiver(pre_save, sender=DeathRecord)
def encrypt_data(sender, instance, **kwargs):
    key = instance.nuber_of_birth if instance.nuber_of_birth else b'9999'
    fernet = Fernet(key)
    instance.first_name = fernet.encrypt(instance.first_name.encode()).decode()
    instance.last_name = fernet.encrypt(instance.last_name.encode()).decode()
    instance.father_name = fernet.encrypt(instance.father_name.encode()).decode()
    instance.mother_name = fernet.encrypt(instance.mother_name.encode()).decode()


'''# decryptor all the data using the nuber_of_birth befour save
@receiver(pre_save, sender=BirthRecord)
def decrypt_data(sender, instance, **kwargs):
    key = instance.nuber_of_birth if instance.nuber_of_birth else b'9999'
    fernet = Fernet(key)
    instance.first_name = fernet.decrypt(instance.first_name.encode()).decode()
    instance.last_name = fernet.decrypt(instance.last_name.encode()).decode()
    instance.father_name = fernet.decrypt(instance.father_name.encode()).decode()
    instance.mother_name = fernet.decrypt(instance.mother_name.encode()).decode()'''