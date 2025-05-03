from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate
from .serializer import BirthRecordSerializer, DeathRecordSerializer
from rest_framework.permissions import IsAuthenticated
from users.users_permissions import IsHospital, IsAPC, IsDSP, IsDSP_Hospital, IsWorker
from drf_spectacular.utils import extend_schema
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
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
    lookup_field = 'birth_number'

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

from .util import generate_birth_certificate_pdf, generate_death_certificate_pdf, sign_pdf
from drf_spectacular.types import OpenApiTypes
class BirthCertificateView(APIView):
    permission_classes = [IsAuthenticated, IsWorker]
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a birth certificate PDF for the given birth_number.",
    )
    def get(self,request, birth_number):
        try:
            birth_certificate = BirthCertificate.objects.get(birth_number=birth_number)
        except BirthCertificate.DoesNotExist:
            return Response({"error": "Birth C not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        data = generate_birth_certificate_pdf(birth_certificate, request.user)
        signed_data  = sign_pdf(data)
        # Save the signed PDF to a file or return it as a response
        response = HttpResponse(signed_data['pdf'], content_type='application/pdf')
        filename = f"birth_certificate_{birth_number}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['X-Signature'] = signed_data['signature']
        return response

class DeathCertificateView(APIView):
    permission_classes = [IsAuthenticated, IsWorker]
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a death certificate PDF for the given birth_number.",
    )
    def get(self,request, birth_number):
        try:
            death_certificate = DeathCertificate.objects.get(birth_number=birth_number)
        except DeathCertificate.DoesNotExist:
            return Response({"error": "Death Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        data = generate_death_certificate_pdf(death_certificate, request.user)
        signed_data  = sign_pdf(data)
        # Save the signed PDF to a file or return it as a response
        response = HttpResponse(signed_data['pdf'], content_type='application/pdf')
        filename = f"death_certificate_{birth_number}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['X-Signature'] = signed_data['signature']
        return response



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