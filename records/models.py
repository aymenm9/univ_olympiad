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
    birth_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Birth Record"

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
    death_cause = models.CharField(max_length=255, null=True)
    rh = models.CharField(max_length=10)
    description = models.TextField(null=True, blank=True)
    age = models.IntegerField(default=0)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    birth_number = models.CharField(max_length=15, unique=True)
    death_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Death Record"


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
    birth_number = models.CharField(max_length=15, unique=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Birth Certificate"

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
    birth_number = models.CharField(max_length=15, unique=True)
    death_number = models.CharField(max_length=15, unique=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Death Certificate"

# -----------------------------------------------------
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(pre_save, sender=BirthRecord)
def add_birth_n(sender, instance, **kwargs):
    year = timezone.now().year
    last_record = BirthRecord.objects.filter(registration_date__year=year).order_by('-id').first()
    number = int(last_record.birth_number.split('-')[1]) if last_record else 1
    instance.birth_number = f"{year}-{number}"


@receiver(post_save, sender=BirthRecord)
def create_certificate(sender, instance, **kwargs):
    certificate = BirthCertificate.objects.filter(birth_number=instance.birth_number).first()
    if certificate:
        if not certificate.is_valid:
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
                birth_number=instance.birth_number,
                is_valid=False
            )
    else:
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


@receiver(pre_save, sender=DeathRecord)
def clc_age_and_update_create_certificate(sender, instance, **kwargs):
    if instance.death_date and instance.birth_date:
        age = instance.death_date.year - instance.birth_date.year
        instance.age = age
    else:
        instance.age = 0
    
    certificate = DeathCertificate.objects.filter(birth_number=instance.birth_number).first()
    if certificate:
        if not certificate.is_valid:
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
                birth_number=instance.birth_number,
                death_number=instance.death_number,
                is_valid=False
            )
    else:
        # create new sertficat
        year = timezone.now().year
        last_record = DeathRecord.objects.filter(registration_date__year=year).order_by('-id').first()
        number = int(last_record.death_number.split('-')[1]) if last_record else 1
        instance.death_number = f"{year}-{number}"
        DeathCertificate.objects.create(
            user=instance.user,
            certificate_number=instance.death_number,
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