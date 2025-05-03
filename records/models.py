from django.db import models
from django.contrib.auth.models import User
from users.models import Hospital
# Create your models here.


class BirthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='birth_records')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_time = models.TimeField()
    registration_date = models.DateField(auto_now=True)
    registration_time = models.TimeField(auto_now=True)
    wilaya = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('male','male'), ('female','female')], default='male')
    rh = models.CharField(max_length=10)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    birth_number = models.AutoField(unique=True, primary_key=True)
    description = models.TextField(null=True, blank=True)

class DeathRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='death_records')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()
    death_time = models.TimeField()
    registration_date = models.DateField(auto_now=True)
    registration_time = models.TimeField(auto_now=True)
    death_wilaya = models.CharField(max_length=100)
    death_commune = models.CharField(max_length=100)
    birth_wilaya = models.CharField(max_length=100)
    birth_commune = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('male','male'), ('female','female')], default='male')
    death_cause = models.CharField(null=True)
    rh = models.CharField(max_length=10)
    description = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    birth_number = models.IntegerField()



class BirthCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    certificate_number = models.IntegerField()
    issue_date = models.DateField(auto_now=True)
    issue_time = models.TimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('male','male'), ('female','female')], default='male')
    birth_date = models.DateField()
    birth_time = models.TimeField()
    birth_wilaya = models.CharField(max_length=100)
    birth_commune = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    birth_number = models.IntegerField(unique=True)


class DeathCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    certificate_number = models.IntegerField()
    issue_date = models.DateField(auto_now=True)
    issue_time = models.TimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('male','male'), ('female','female')], default='male')
    birth_date = models.DateField()
    death_date = models.DateField()
    death_time = models.TimeField()
    birth_wilaya = models.CharField(max_length=100)
    birth_commune = models.CharField(max_length=100)
    death_wilaya = models.CharField(max_length=100)
    death_commune = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    birth_number = models.IntegerField(unique=True)



from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
@receiver(pre_save, sender=DeathRecord)
def clc_age_and_update_create_certificate(sender, instance, **kwargs):
    if instance.death_date and instance.birth_date:
        age = instance.death_date.year - instance.birth_date.year
        instance.age = age
    else:
        instance.age = 0
    
    certificate = DeathCertificate.objects.filter(birth_number=instance.birth_number).first()
    if certificate:
        # if it exists, update all certificate info
        certificate.objects.update(
            user=instance.user,
            certificate_number=instance.birth_number,
            first_name=instance.first_name,
            last_name=instance.last_name,
            sex=instance.sex,
            birth_date=instance.birth_date,
            death_date=instance.death_date,
            death_time=instance.death_time,
            birth_wilaya=instance.birth_wilaya,
            birth_commune=instance.birth_commune,
            death_wilaya=instance.death_wilaya,
            death_commune=instance.death_commune,
            father_name=instance.father_name,
            mother_name=instance.mother_name,
            birth_number=instance.birth_number
        )
    else:
        # create new sertficat
        DeathCertificate.objects.create(
            user=instance.user,
            certificate_number=instance.birth_number,
            first_name=instance.first_name,
            last_name=instance.last_name,
            sex=instance.sex,
            birth_date=instance.birth_date,
            death_date=instance.death_date,
            death_time=instance.death_time,
            birth_wilaya=instance.birth_wilaya,
            birth_commune=instance.birth_commune,
            death_wilaya=instance.death_wilaya,
            death_commune=instance.death_commune,
            father_name=instance.father_name,
            mother_name=instance.mother_name,
            birth_number=instance.birth_number
        )

@receiver(post_save, sender=BirthRecord)
def create_certificate(sender, instance, **kwargs):
    certificate = BirthCertificate.objects.filter(birth_number=instance.birth_number).first()
    if certificate:
        # if it exists, update all certificate info
        certificate.objects.update(
            user=instance.user,
            certificate_number=instance.birth_number,
            first_name=instance.first_name,
            last_name=instance.last_name,
            birth_date=instance.birth_date,
            birth_time=instance.birth_time,
            birth_wilaya=instance.wilaya,
            birth_commune=instance.commune,
            father_name=instance.father_name,
            mother_name=instance.mother_name,
            birth_number=instance.birth_number
        )
    else:
        # create new sertficat
        BirthCertificate.objects.create(
            user=instance.user,
            certificate_number=instance.birth_number,
            first_name=instance.first_name,
            last_name=instance.last_name,
            birth_date=instance.birth_date,
            birth_time=instance.birth_time,
            birth_wilaya=instance.wilaya,
            birth_commune=instance.commune,
            father_name=instance.father_name,
            mother_name=instance.mother_name,
            birth_number=instance.birth_number
        )
'''
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
    load_dotenv()
    key = os.getenv('FERNET_KEY')
    fernet = Fernet(key)
    instance.first_name = fernet.encrypt(instance.first_name.encode()).decode()
    instance.last_name = fernet.encrypt(instance.last_name.encode()).decode()
    instance.father_name = fernet.encrypt(instance.father_name.encode()).decode()
    instance.mother_name = fernet.encrypt(instance.mother_name.encode()).decode()'''


'''# decryptor all the data using the nuber_of_birth befour save
@receiver(pre_save, sender=BirthRecord)
def decrypt_data(sender, instance, **kwargs):
    key = instance.nuber_of_birth if instance.nuber_of_birth else b'9999'
    fernet = Fernet(key)
    instance.first_name = fernet.decrypt(instance.first_name.encode()).decode()
    instance.last_name = fernet.decrypt(instance.last_name.encode()).decode()
    instance.father_name = fernet.decrypt(instance.father_name.encode()).decode()
    instance.mother_name = fernet.decrypt(instance.mother_name.encode()).decode()'''