from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer, LoginSerializer, CreateHospitalSerializer, hospitalSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .users_permissions import IsDSP, IsAdmin
from .models import Hospital, UserInfo
from django.contrib.auth.models import User
# Create your views here.


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={200: UserSerializer},
    )

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateHospitalView(APIView):
    permission_classes = [IsAuthenticated, IsDSP, IsAdmin]
    
    @extend_schema(
        request=CreateHospitalSerializer,
        responses={201: hospitalSerializer},
    )
    def post(self, request):
        serializer = CreateHospitalSerializer(data=request.data)
        if serializer.is_valid():
            hospital_info = serializer.validated_data['hospital']
            hospital = Hospital.objects.create(
                name=hospital_info['name'],
                wilaya=hospital_info['wilaya'],
                commune=hospital_info['commune'],
                address=hospital_info['address'],
                phone_number=hospital_info['phone_number'],
                email=hospital_info['email'],
                dsp=request.user.info.dsp
            )
            admin = User.objects.create_user(
                username=hospital_info['name'],
                password=serializer.validated_data['password'],
                first_name=hospital_info['name'],
                last_name='Admin'
            )
            user_info = UserInfo.objects.create(
                user=admin,
                Organization='Hospital',
                hospital=hospital,
                role='Admin'
            )
            hospital_serializer = hospitalSerializer(hospital)
            return Response(hospital_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
