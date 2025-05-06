from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo, Hospital, APC, DSP


class hospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'dsp': {'read_only': True},
            'wilaya': {'read_only': True},
            'commune': {'read_only': True},
        }

class APCSerializer(serializers.ModelSerializer):
    class Meta:
        model = APC
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'dsp': {'read_only': True},
            'wilaya': {'read_only': True},
            'commune': {'read_only': True},
        }
    
class DSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = DSP
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }

class admin_info(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
class CreateAPCSerializer(serializers.Serializer):
    apc = APCSerializer()
    admin = admin_info()

class CreateHospitalSerializer(serializers.Serializer):
    hospital = hospitalSerializer()
    admin = admin_info()


class chatHistorySerializer(serializers.Serializer):

    message = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'hospital':{'read_only': True},
            'dsp':{'read_only': True},
            'apc':{'read_only': True},
            'Organization':{'read_only': True}
        }



class UserSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(source='info')
    organization_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'user_info', 'organization_info']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'organization': {'read_only': True},

        }

    def get_organization_info(self, obj):
        info = getattr(obj, 'info', None)
        if info:
            org = info.get_organization()
            if org:
                return {
                    'id': org.id,
                    'name': org.name,
                    'wilaya': org.wilaya,
                    'commune': getattr(org, 'commune', None),  # not all orgs may have this
                    'type': info.Organization
                }
        return None
    
class LoginSerializer(serializers.Serializer):
    user = UserSerializer
    access = serializers.CharField()
    refresh = serializers.CharField()