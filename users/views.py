from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import (UserSerializer, LoginSerializer,
                        CreateHospitalSerializer, hospitalSerializer, 
                        chatHistorySerializer, ChangePasswordSerializer,
                        CreateAPCSerializer, APCSerializer,
                        CourtSerializer, CreateCourtSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .users_permissions import IsDSP, IsAdmin, IsDSP_APC, IsWorker, IsDSP_Court
from .models import Hospital, UserInfo, APC, DSP, Court
from django.contrib.auth.models import User
from .chat_bot import chatbot
from .models import ChatHistory
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

class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name','last_name'] 

    def get_queryset(self):
        if self.request.user.info.Organization == 'Hospital':
            return super().get_queryset().filter(info__hospital=self.request.user.info.hospital)
        elif self.request.user.info.Organization == 'APC':
            return super().get_queryset().filter(info__apc=self.request.user.info.apc)
        elif self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(info__dsp=self.request.user.info.dsp)

    def perform_create(self, serializer):
        user = User.objects.create_user(
            username=self.request.data['username'],
            password=self.request.data['password'],
            first_name=self.request.data['first_name'],
            last_name=self.request.data['last_name'],
            email=self.request.data['email']
        )
        user_info = UserInfo.objects.create(
                user=user,
                Organization=self.request.user.info.Organization,
                role=self.request.data['user_info']['role'],
                hospital=self.request.user.info.hospital,
                apc=self.request.user.info.apc,
                dsp=self.request.user.info.dsp
            )
        user.info = user_info
        user_ser = UserSerializer(user)
        return Response(user_ser.data, status=status.HTTP_201_CREATED)
            

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        if self.request.user.info.Organization == 'Hospital':
            return super().get_queryset().filter(info__hospital=self.request.user.info.hospital)
        elif self.request.user.info.Organization == 'APC':
            return super().get_queryset().filter(info__apc=self.request.user.info.apc)
        elif self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(info__dsp=self.request.user.info.dsp)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: UserSerializer},
    )
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            apc = hospital_info['apc']
            hospital = Hospital.objects.create(
                name=hospital_info['name'],
                wilaya=apc.wilaya,
                commune=apc.commune,
                apc=apc,
                address=hospital_info['address'],
                phone_number=hospital_info['phone_number'],
                email=hospital_info['email'],
                dsp=request.user.info.dsp
            )
            admin = User.objects.create_user(
                username=serializer.validated_data['admin']['username'],
                password=serializer.validated_data['admin']['password'],
                first_name=hospital_info['name'],
                last_name='Admin',
                email=hospital_info['email']
            )
            user_info = UserInfo.objects.create(
                user=admin,
                Organization='Hospital',
                hospital=hospital,
                role='Admin',
            )
            hospital_serializer = hospitalSerializer(hospital)
            return Response(hospital_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalView(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = hospitalSerializer
    permission_classes = [IsAuthenticated, IsWorker]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'wilaya','commune','phone_number','email'] 

    def get_queryset(self):
        if self.request.user.info.Organization == 'Hospital':
            return super().get_queryset().filter(id=self.request.user.info.hospital.id)
        elif self.request.user.info.Organization == 'APC':
            return super().get_queryset().filter(apc=self.request.user.info.apc)
        elif self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(dsp=self.request.user.info.dsp)

class CreateAPCView(APIView):
    permission_classes = [IsAuthenticated, IsDSP, IsAdmin]
    
    @extend_schema(
        request=CreateAPCSerializer,
        responses={201: APCSerializer},
    )
    def post(self, request):
        serializer = CreateAPCSerializer(data=request.data)
        if serializer.is_valid():
            apc_info = serializer.validated_data['apc']
            apc = APC.objects.create(
                name=apc_info['name'],
                wilaya=request.user.info.dsp.wilaya,
                commune=apc_info['name'],
                address=apc_info['address'],
                phone_number=apc_info['phone_number'],
                email=apc_info['email'],
                dsp=request.user.info.dsp
            )
            admin = User.objects.create_user(
                username=serializer.validated_data['admin']['username'],
                password=serializer.validated_data['admin']['password'],
                first_name=apc_info['name'],
                last_name='Admin',
                email=apc_info['email']
            )
            user_info = UserInfo.objects.create(
                user=admin,
                Organization='APC',
                apc=apc,
                role='Admin'
            )
            apc_serializer = APCSerializer(apc)
            return Response(apc_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class APCView(generics.ListAPIView):
    queryset = APC.objects.all()
    serializer_class = APCSerializer
    permission_classes = [IsAuthenticated, IsDSP_APC,IsWorker]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'wilaya','commune','phone_number','email'] 

    def get_queryset(self):
        if self.request.user.info.Organization == 'APC':
            return super().get_queryset().filter(id=self.request.user.info.apc.id)
        elif self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(dsp=self.request.user.info.dsp)


class CreateCourtView(APIView):
    permission_classes = [IsAuthenticated, IsDSP, IsAdmin]
    
    @extend_schema(
        request=CreateCourtSerializer,
        responses={201: CourtSerializer},
    )
    def post(self, request):
        serializer = CreateCourtSerializer(data=request.data)
        if serializer.is_valid():
            court_info = serializer.validated_data['court']
            court = Court.objects.create(
                name=court_info['name'],
                wilaya=request.user.info.dsp.wilaya,
                address=court_info['address'],
                phone_number=court_info['phone_number'],
                email=court_info['email'],
                dsp=request.user.info.dsp
            )
            admin = User.objects.create_user(
                username=serializer.validated_data['admin']['username'],
                password=serializer.validated_data['admin']['password'],
                first_name=court_info['name'],
                last_name='Admin',
                email=court_info['email']
            )
            user_info = UserInfo.objects.create(
                user=admin,
                Organization='Court',
                court=court,
                role='Admin'
            )
            court_serializer = CourtSerializer(court)
            return Response(court_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourtView(generics.ListAPIView):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    permission_classes = [IsAuthenticated, IsDSP_Court,IsWorker]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'wilaya','phone_number','email'] 

    def get_queryset(self):
        if self.request.user.info.Organization == 'Court':
            return super().get_queryset().filter(id=self.request.user.info.court.id)
        elif self.request.user.info.Organization == 'DSP':
            return super().get_queryset().filter(dsp=self.request.user.info.dsp)


class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=chatHistorySerializer,
        responses={200: chatHistorySerializer},
    )
    def post(self, request):
        user = request.user
        chat_history, _ = ChatHistory.objects.get_or_create(user=user)

        history = chat_history.msg[-10:]

        response = chatbot(request.data['message'], history)

        chat_history.msg.append({
            "role": "user",
            "parts": [{"text": request.data['message']}]
        })
        chat_history.msg.append({
            "role": "model",
            "parts": [{"text": response}]
        })
        chat_history.save()

        return Response({'message': response}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        chat_history, _ = ChatHistory.objects.get_or_create(user=user)
        history = chat_history.msg[:10]
        return Response(history, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        chat_history, _ = ChatHistory.objects.get_or_create(user=user)
        chat_history.msg = []
        chat_history.save()
        return Response({}, status=status.HTTP_200_OK)