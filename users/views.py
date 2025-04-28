from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={200: UserSerializer},
    )

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.id)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role
        }, status=status.HTTP_200_OK)

