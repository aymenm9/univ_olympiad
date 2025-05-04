from rest_framework import serializers
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate

class BirthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False},
            'birth_number': {'read_only': True},
        }
        read_only_fields = ['user','hospital','id']


class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False},
            'age': {'required': False},
            'death_number': {'read_only': True},
        }
        read_only_fields = ['user','hospital','id']

class BirthCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthCertificate
        fields = '__all__'
        read_only_fields = ['user','id']

class DeathCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathCertificate
        fields = '__all__'
        read_only_fields = ['user','id']