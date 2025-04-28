from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BirthRecord, DeathRecord
from .serializer import BirthRecordSerializer, DeathRecordSerializer
from rest_framework.permissions import IsAuthenticated
from users.users_permissions import IsHospital, IsDSP_APC
from drf_spectacular.utils import extend_schema
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
# Create your views here.

class BirthRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHospital]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class BirthRecordDetailView(generics.RetrieveAPIView):
    load_dotenv()
    permission_classes = [IsAuthenticated]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()
    lookup_field = 'nuber_of_birth'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.role == 'APC' or self.request.user.role == 'DSP':
            key = os.getenv('FERNET_KEY')
            fernet = Fernet(key)
            obj.first_name = fernet.decrypt(obj.first_name.encode()).decode()
            obj.last_name = fernet.decrypt(obj.last_name.encode()).decode()
            obj.father_name = fernet.decrypt(obj.father_name.encode()).decode()
            obj.mother_name = fernet.decrypt(obj.mother_name.encode()).decode()
            
        return obj


class DeathRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHospital]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class DeathRecordDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsDSP_APC]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()
    lookup_field = 'nuber_of_birth'

    def get_object(self):
        obj = super().get_object()
        if self.request.user.role == 'APC' or self.request.user.role == 'DSP':
            key = os.getenv('FERNET_KEY')
            fernet = Fernet(key)
            obj.first_name = fernet.decrypt(obj.first_name.encode()).decode()
            obj.last_name = fernet.decrypt(obj.last_name.encode()).decode()
            obj.father_name = fernet.decrypt(obj.father_name.encode()).decode()
            obj.mother_name = fernet.decrypt(obj.mother_name.encode()).decode()
        # creat this data to pdf

        

        # and send it to the user outh saving
            
        return obj