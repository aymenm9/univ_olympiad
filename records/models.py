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
