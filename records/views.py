from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate
from .serializer import BirthRecordSerializer, DeathRecordSerializer, BirthCertificateSerializer, DeathCertificateSerializer, StatisticSerializer
from rest_framework.permissions import IsAuthenticated
from users.users_permissions import IsHospital, IsAPC, IsDSP, IsDSP_Hospital, IsWorker, IsAdmin, IsDSP_APC
from drf_spectacular.utils import extend_schema
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.

class BirthRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsHospital, IsWorker]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()

    def get_queryset(self):
        if self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(hospital__dsp=self.request.user.info.dsp)
        return super().get_queryset().filter(hospital=self.request.user.info.hospital)

    def perform_create(self, serializer):
        user = self.request.user
        hospital = user.info.hospital
        wilaya = hospital.wilaya  
        commune = hospital.commune
        year = timezone.now().year
        last_record = BirthRecord.objects.filter(registration_date__year=year).order_by('-id').first()
        number = int(last_record.birth_number.split('-')[1])+1 if last_record else 1
        birth_number = f"{year}-{number}"
        birth_record = serializer.save(
            user=user,
            hospital=hospital,
            wilaya=wilaya,
            commune=commune,
            birth_number=birth_number
        )
        certificate = BirthCertificate.objects.create(
            user=user,
            certificate_number=birth_number,
            first_name=birth_record.first_name,
            last_name=birth_record.last_name,
            sex=birth_record.sex,
            birth_date=birth_record.birth_date,
            birth_time=birth_record.birth_time,
            birth_wilaya=birth_record.wilaya,
            birth_commune=birth_record.commune,
            father_name=birth_record.father_name,
            mother_name=birth_record.mother_name,
            birth_number=birth_record.birth_number
        )
        return birth_record
    
class BirthRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()
    lookup_field = 'birth_number'

    def get_queryset(self):
        if self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(hospital__dsp=self.request.user.info.dsp)
        return super().get_queryset().filter(hospital=self.request.user.info.hospital)
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)

class DeathRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()

    def get_queryset(self):
        if self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(hospital__dsp=self.request.user.info.dsp)
        return super().get_queryset().filter(hospital=self.request.user.info.hospital)

    def perform_create(self, serializer):
        user = self.request.user
        hospital = user.info.hospital
        wilaya = hospital.wilaya
        commune = hospital.commune

        year = timezone.now().year
        last_record = DeathRecord.objects.filter(registration_date__year=year).order_by('-id').first()
        number = int(last_record.death_number.split('-')[1])+1 if last_record else 1
        death_number = f"{year}-{number}"
        death_record = serializer.save(
            user=user,
            hospital=hospital,
            death_wilaya=wilaya,
            death_commune=commune,
            death_number=death_number
        )

        certificate = DeathCertificate.objects.create(
            user=user,
            certificate_number=number,
            first_name=death_record.first_name,
            last_name=death_record.last_name,
            sex=death_record.sex,
            birth_date=death_record.birth_date,
            death_date=death_record.death_date,
            death_time=death_record.death_time,
            birth_wilaya=death_record.birth_wilaya,
            birth_commune=death_record.birth_commune,
            death_wilaya=death_record.death_wilaya,
            death_commune=death_record.death_commune,
            father_name=death_record.father_name,
            mother_name=death_record.mother_name,
            birth_number=death_record.birth_number,
            death_number=death_record.death_number
        )

        return death_record



class DeathRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()
    lookup_field = 'death_number'

    def get_queryset(self):
        if self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(hospital__dsp=self.request.user.info.dsp)
        return super().get_queryset().filter(hospital=self.request.user.info.hospital)
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)

from .util import generate_birth_certificate_pdf, generate_death_certificate_pdf, sign_pdf
from drf_spectacular.types import OpenApiTypes



class BirthCertificateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWorker, IsDSP_APC]
    serializer_class = BirthCertificateSerializer
    queryset = BirthCertificate.objects.all()

class BirthCertificateDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsWorker, IsDSP_APC]
    serializer_class = BirthCertificateSerializer
    queryset = BirthCertificate.objects.all()
    lookup_field = 'birth_number'

class BirthCertificateConfirm(APIView):
    permission_classes = [IsAuthenticated, IsWorker, IsAPC]
    def post(self, request, birth_number):
        try:
            
            birth_certificate = BirthCertificate.objects.get(birth_number=birth_number)
        except BirthCertificate.DoesNotExist:
            return Response({"error": "Birth Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate the birth certificate
        birth_certificate.is_valid = True
        birth_certificate.user = request.user
        birth_certificate.save()
        return Response({"message": "Birth Certificate is valid."}, status=status.HTTP_200_OK)



class BirthCertificatePDF(APIView):
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


class DeathCertificateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWorker, IsDSP_APC]
    serializer_class = DeathCertificateSerializer
    queryset = DeathCertificate.objects.all()

class DeathCertificateDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsWorker, IsDSP_APC]
    serializer_class = DeathCertificateSerializer
    queryset = DeathCertificate.objects.all()
    lookup_field = 'death_number'

class DeathCertificateConfirm(APIView):
    permission_classes = [IsAuthenticated, IsWorker, IsAPC]
    def post(self, request, death_number):
        try:
            
            death_certificate = DeathCertificate.objects.get(death_number=death_number)
        except DeathCertificate.DoesNotExist:
            return Response({"error": "death Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate the birth certificate
        death_certificate.is_valid = True
        death_certificate.user = request.user
        death_certificate.save()
        return Response({"message": "death Certificate is valid."}, status=status.HTTP_200_OK)
class DeathCertificatePDf(APIView):
    permission_classes = [IsAuthenticated, IsWorker]
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a death certificate PDF for the given death_number.",
    )
    def get(self,request, death_number):
        try:
            death_certificate = DeathCertificate.objects.get(death_number=death_number)
        except DeathCertificate.DoesNotExist:
            return Response({"error": "Death Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        data = generate_death_certificate_pdf(death_certificate, request.user)
        signed_data  = sign_pdf(data)
        # Save the signed PDF to a file or return it as a response
        response = HttpResponse(signed_data['pdf'], content_type='application/pdf')
        filename = f"death_certificate_{death_number}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['X-Signature'] = signed_data['signature']
        return response


class StatisticView(APIView):
    permission_classes=[IsAuthenticated, IsWorker]

    @extend_schema(
        request=None,
        responses={200:StatisticSerializer} 
    )
    def get(self,request):
        death,birth= 0,0
        if request.user.info.Organization == 'Hospital':
            death = DeathRecord.objects.filter(hospital=request.user.info.hospital).count()
            birth = BirthRecord.objects.filter(hospital=request.user.info.hospital).count()
        elif request.user.info.Organization == 'APC':
            death = DeathCertificate.objects.filter(death_commune=request.user.info.apc.commune).count()
            birth = BirthCertificate.objects.filter(birth_commune=request.user.info.apc.commune).count()
        elif request.user.info.Organization == 'DSP':
            death = DeathCertificate.objects.filter(death_wilaya=request.user.info.apc.wilaya).count()
            birth = BirthCertificate.objects.filter(birth_wilaya=request.user.info.apc.wilaya).count()  

        total = death + birth

        data = StatisticSerializer({
            "death": death,
            "birth": birth,
            "total": total
        })
        return Response(data.data,status=status.HTTP_200_OK)
        


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