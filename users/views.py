from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer, LoginSerializer,chatHistorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .chatbot import chatbot

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

