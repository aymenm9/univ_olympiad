from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name','role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    
class LoginSerializer(serializers.Serializer):
    user = UserSerializer
    access = serializers.CharField()
    refresh = serializers.CharField()