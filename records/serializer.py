from rest_framework import serializers
from .models import BirthRecord, DeathRecord

class BirthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
        }
        read_only_fields = ['user','id']


class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
        }
        read_only_fields = ['user','id']

class BirthRecordCertificateSerializer(serializers.Serializer):
    signature= serializers.CharField()
    record = BirthRecordSerializer()

class DethRecordCertificateSerializer(serializers.Serializer):
    signature= serializers.CharField()
    record = DeathRecordSerializer()