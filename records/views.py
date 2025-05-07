from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import status
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate, BurialPermit
from .serializer import (BirthRecordSerializer, DeathRecordSerializer, 
                         BirthCertificateSerializer, DeathCertificateSerializer, 
                         StatisticSerializer, PublicBirthCertificateSerializer, 
                         PublicDeathCertificateSerializer,
                         BirthCertificateUpdateRequestSerializer,
                         DeathCertificateUpdateRequestSerializer,
                         BurialPermitSerializer)
from rest_framework.permissions import IsAuthenticated
from users.users_permissions import IsHospital, IsAPC, IsDSP, IsDSP_Hospital, IsWorker, IsAdmin, IsDSP_APC, IsDSP_Court, IsCourt
from drf_spectacular.utils import extend_schema
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.utils import timezone
from collections import OrderedDict
# Create your views here.

class BirthRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = BirthRecordSerializer
    queryset = BirthRecord.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['birth_number', 'first_name','last_name'] 

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
        certificate = BirthCertificate.objects.get(birth_number=self.kwargs['birth_number'])
        if certificate.is_valid:
            return Response({"error": "Certificate is already valid."}, status=status.HTTP_400_BAD_REQUEST)
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)

class DeathRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDSP_Hospital, IsWorker]
    serializer_class = DeathRecordSerializer
    queryset = DeathRecord.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['birth_number', 'first_name','last_name', 'death_number'] 

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
        certificate = DeathCertificate.objects.get(death_number=self.kwargs['death_number'])
        if certificate.is_valid:
            return Response({"error": "Certificate is already valid."}, status=status.HTTP_400_BAD_REQUEST)
        return serializer.save(user=self.request.user, hospital=self.request.user.info.hospital)

from .util import generate_birth_certificate_pdf, generate_death_certificate_pdf, sign_pdf, generate_burial_permit_pdf
from drf_spectacular.types import OpenApiTypes



class BirthCertificateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWorker, IsDSP_APC]
    serializer_class = BirthCertificateSerializer
    queryset = BirthCertificate.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['birth_number', 'first_name','last_name'] 
    

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['birth_number', 'first_name','last_name','death_number'] 

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
        
        death_record = DeathRecord.objects.get(death_number=death_number)
        death_certificate.is_valid = True
        death_certificate.user = request.user
        death_certificate.save()
        approved = death_record.death_type == 'natural'
        permit = BurialPermit.objects.create(
            user=request.user,
            record=death_record,
            certificate=death_certificate,
            approved=approved
        )
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

class BurialPermitView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWorker]
    serializer_class = BurialPermitSerializer
    queryset = BurialPermit.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['record__death_number', 'record__first_name','record__last_name']

    def get_queryset(self):
        if self.request.user.info.Organization == 'Court':
            return BurialPermit.objects.filter(record__Hospital__wilaya=self.request.user.info.get_organization().wilaya).filter(approved=False)
        return BurialPermit.objects.filter(approved=True)

class BurialPermitconfirmView(APIView):
    permission_classes = [IsAuthenticated, IsWorker, IsCourt]
    def post(self, request, death_number):
        try:
            burial_permit = BurialPermit.objects.get(record__death_number=death_number)
        except BurialPermit.DoesNotExist:
            return Response({"error": "Burial Permit not found."}, status=status.HTTP_404_NOT_FOUND)
        
        burial_permit.is_valid = True
        burial_permit.user = request.user
        burial_permit.save()
        return Response({"message": "Burial Permit is valid."}, status=status.HTTP_200_OK)

class BurialPermitPdfView(APIView):
    permission_classes = [IsAuthenticated, IsWorker]
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a Burial Permit PDF for the given death_number.",
    )
    def get(self,request, death_number):
        try:
            burial_permit = BurialPermit.objects.get(record__death_number=death_number)
        except BurialPermit.DoesNotExist:
            return Response({"error": "Burial Permit not found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = generate_burial_permit_pdf(burial_permit, request.user)
        signed_data  = sign_pdf(data)
        # Save the signed PDF to a file or return it as a response
        response = HttpResponse(signed_data['pdf'], content_type='application/pdf')
        filename = f"burial_permit_{death_number}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['X-Signature'] = signed_data['signature']
        return response

class PublicBirthCertificatePDf(APIView):
    @extend_schema(
        request=PublicBirthCertificateSerializer,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a birth certificate PDF for the given birth_number.",
    )
    def post(self,request):
        serializer = PublicBirthCertificateSerializer(data=request.data)
        if serializer.is_valid():
            birth_number = serializer.validated_data['birth_number']
            try:
                birth_certificate = BirthCertificate.objects.get(birth_number=birth_number)
            except BirthCertificate.DoesNotExist:
                return Response({"error": "Birth Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if(
                birth_certificate.first_name != serializer.validated_data['first_name'] 
                or birth_certificate.last_name != serializer.validated_data['last_name'] 
                or birth_certificate.birth_date != serializer.validated_data['birth_date'] 
                or birth_certificate.birth_wilaya != serializer.validated_data['birth_wilaya'] 
                or birth_certificate.father_name != serializer.validated_data['father_name'] 
                or birth_certificate.mother_name != serializer.validated_data['mother_name'] 
            ):
                return Response({"error": "Birth Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
            
            data = generate_birth_certificate_pdf(birth_certificate)
            signed_data  = sign_pdf(data)
            # Save the signed PDF to a file or return it as a response
            response = HttpResponse(signed_data['pdf'], content_type='application/pdf')
            filename = f"birth_certificate_{birth_number}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['X-Signature'] = signed_data['signature']
            return response

class PublicDeathCertificatePDf(APIView):
    @extend_schema(
        request=PublicDeathCertificateSerializer,
        responses={200: OpenApiTypes.BINARY},
        description="Generate a death certificate PDF for the given death_number.",
    )
    def post(self,request):
        serializer = PublicDeathCertificateSerializer(data=request.data)
        if serializer.is_valid():
            death_number = serializer.validated_data['death_number']
            try:
                death_certificate = DeathCertificate.objects.get(death_number=death_number)
            except DeathCertificate.DoesNotExist:
                return Response({"error": "Death Certificate not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if(
                death_certificate.first_name != serializer.validated_data['first_name'] 
                or death_certificate.last_name != serializer.validated_data['last_name'] 
                or death_certificate.birth_date != serializer.validated_data['birth_date'] 
                or death_certificate.death_date != serializer.validated_data['death_date'] 
                or death_certificate.death_wilaya != serializer.validated_data['death_wilaya'] 
                or death_certificate.father_name != serializer.validated_data['father_name'] 
                or death_certificate.mother_name != serializer.validated_data['mother_name']) : 
                return Response({"error": "one of the Invalid input."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)

        data = generate_death_certificate_pdf(death_certificate)
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
        current_year = timezone.now().year
        death,birth= 0,0
        if request.user.info.Organization == 'Hospital':
            death = DeathRecord.objects.filter(hospital=request.user.info.hospital).count()
            birth = BirthRecord.objects.filter(hospital=request.user.info.hospital).count()
        elif request.user.info.Organization == 'APC':
            death = DeathCertificate.objects.filter(death_commune=request.user.info.apc.commune).count()
            birth = BirthCertificate.objects.filter(birth_commune=request.user.info.apc.commune).count()
        elif request.user.info.Organization == 'DSP':
            death = DeathCertificate.objects.filter(death_wilaya=request.user.info.dsp.wilaya).count()
            birth = BirthCertificate.objects.filter(birth_wilaya=request.user.info.dsp.wilaya).count()  

        total = death + birth

        data = StatisticSerializer({
            "death": death,
            "birth": birth,
            "total": total
        })
        return Response(data.data,status=status.HTTP_200_OK)
        
class MonthlyStatisticView(APIView):
    permission_classes = [IsAuthenticated, IsWorker]

    @extend_schema(
        request=None,
        responses={200: StatisticSerializer(many=True)}
    )
    def get(self, request):
        current_year = timezone.now().year
        stats_by_month = OrderedDict()
        org = request.user.info.Organization

        for month in range(1, 13):
            if org == 'Hospital':
                death = DeathRecord.objects.filter(
                    hospital=request.user.info.hospital,
                    death_date__year=current_year,
                    death_date__month=month
                ).count()
                birth = BirthRecord.objects.filter(
                    hospital=request.user.info.hospital,
                    birth_date__year=current_year,
                    birth_date__month=month
                ).count()

            elif org == 'APC':
                death = DeathCertificate.objects.filter(
                    death_commune=request.user.info.apc.commune,
                    death_date__year=current_year,
                    death_date__month=month
                ).count()
                birth = BirthCertificate.objects.filter(
                    birth_commune=request.user.info.apc.commune,
                    birth_date__year=current_year,
                    birth_date__month=month
                ).count()

            elif org == 'DSP':
                death = DeathCertificate.objects.filter(
                    death_wilaya=request.user.info.dsp.wilaya,
                    death_date__year=current_year,
                    death_date__month=month
                ).count()
                birth = BirthCertificate.objects.filter(
                    birth_wilaya=request.user.info.dsp.wilaya,
                    birth_date__year=current_year,
                    birth_date__month=month
                ).count()

            stats_by_month[month] = {
                "death": death,
                "birth": birth,
                "total": death + birth
            }

        # Serialize each month's data
        serialized_data = {
            month: StatisticSerializer(data).data for month, data in stats_by_month.items()
        }

        return Response(serialized_data, status=status.HTTP_200_OK)

class StatisticViewV2(APIView):
    def get(self, request):
        deths_causes_count= {}
        if request.user.info.Organization == 'Hospital':
            deaths = DeathRecord.objects.filter(hospital=request.user.info.hospital).all()
        elif request.user.info.Organization == 'APC':
            deaths = DeathCertificate.objects.filter(death_commune=request.user.info.apc.commune).all()
        elif request.user.info.Organization == 'DSP':
            deaths = DeathCertificate.objects.filter(death_wilaya=request.user.info.dsp.wilaya).all()
        
        for death in deaths:
            deths_causes_count[death.death_cause] = deths_causes_count.get(death.death_cause, 0) + 1
        
        return Response(deths_causes_count, status=status.HTTP_200_OK)



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