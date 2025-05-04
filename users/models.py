from django.contrib.auth.models import User
from django.db import models


class DSP(models.Model):
    name = models.CharField(max_length=100)
    wilaya = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'DSP of : {self.name} wilaya: {self.wilaya}'

class APC(models.Model):
    dsp = models.ForeignKey(DSP, on_delete=models.CASCADE, related_name='apcs')
    name = models.CharField(max_length=100)
    wilaya = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'APC of : {self.name} wilaya: {self.wilaya} commune: {self.commune}'


class Hospital(models.Model):
    dsp = models.ForeignKey(DSP, on_delete=models.CASCADE, related_name='hospitals')
    apc = models.ForeignKey(APC, on_delete=models.CASCADE, related_name='hospitals')
    name = models.CharField(max_length=100)
    wilaya = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'Hospital of : {self.name} wilaya: {self.wilaya} commune: {self.commune}'
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    Organization = models.CharField(choices=[
        ('Hospital','Hospital'),
        ('DSP','DSP'),
        ('APC','APC')
    ], max_length=50, default='Hospital')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    dsp = models.ForeignKey(DSP, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    apc = models.ForeignKey(APC, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    role = models.CharField(choices=[
        ('Admin', 'Admin'),
        ('Worker', 'Worker'),
        ('Guest', 'Guest'),
    ], max_length=20, default='Guest')

    def __str__(self):
        org_name =''
        if self.Organization == 'Hospital':
            org_name = self.hospital.name
        elif self.Organization == 'DSP':
            org_name = self.dsp.name
        elif self.Organization == 'APC':
            org_name = self.apc.name
        
        return f'{self.user.username} - {self.role} - {self.Organization} - {org_name}'
    
    def get_organization(self):
        if self.Organization == 'Hospital':
            return self.hospital
        elif self.Organization == 'DSP':
            return self.dsp
        elif self.Organization == 'APC':
            return self.apc
        else:
            return None


class ChatHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_history')
    msg = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user}, {self.msg}'