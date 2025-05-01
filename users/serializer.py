from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo, Hospital


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user', 'Organization', 'role']
        extra_kwargs = {
            'user': {'read_only': True},
        }
class UserSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    
class LoginSerializer(serializers.Serializer):
    user = UserSerializer
    access = serializers.CharField()
    refresh = serializers.CharField()