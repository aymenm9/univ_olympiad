from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BirthRecord, DeathRecord
from .serializer import BirthRecordSerializer, DeathRecordSerializer
from rest_framework.permissions import IsAuthenticated
from users.users_permissions import IsHospital, IsAPC, IsDSP, IsDSP_Hospital, IsWorker
from drf_spectacular.utils import extend_schema
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
# Create your views here.

class BirthRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()

    def get_queryset(self):
        if self.request.user.info.role == 'DSP':
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)
    
class BirthRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()
    lookup_field = 'birth_number'

    def get_queryset(self):
        if self.request.user.info.role == 'DSP':
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)

class DeathRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHospital]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class DeathRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()
    lookup_field = 'nuber_of_birth'

    def get_object(self):
        load_dotenv()
        obj = super().get_object()
        if self.request.user.role == 'APC' or self.request.user.role == 'DSP':
            key = os.getenv('FERNET_KEY')
            fernet = Fernet(key)
            obj.first_name = fernet.decrypt(obj.first_name.encode()).decode()
            obj.last_name = fernet.decrypt(obj.last_name.encode()).decode()
            obj.father_name = fernet.decrypt(obj.father_name.encode()).decode()
            obj.mother_name = fernet.decrypt(obj.mother_name.encode()).decode()
      
        return obj


from .gen import generate

class AiView(APIView):
    permission_classes = [IsAuthenticated, IsHospital]
    @extend_schema(
        request=None,
        responses={200: str},
        description="Generate a death certificate PDF for the given nuber_of_birth.",
    )
    def get(self,request):
        try:

            death_record = DeathRecord.objects.all()
        except DeathRecord.DoesNotExist:
            return Response({"error": "Death record not found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = generate(death_record)
        return Response(data, status=status.HTTP_200_OK)