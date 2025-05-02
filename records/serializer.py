from rest_framework import serializers
from .models import BirthRecord, DeathRecord

class BirthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False},
        }
        read_only_fields = ['user','hospital','id']


class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False},
            'age': {'required': False}
        }
        read_only_fields = ['user','hospital','id']

class BirthCertificate(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = '__all__'
        read_only_fields = ['user','id']

class DeathCertificate(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = '__all__'
        read_only_fields = ['user','id']