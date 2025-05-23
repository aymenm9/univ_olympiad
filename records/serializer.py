from rest_framework import serializers
from .models import BirthRecord, DeathRecord, BirthCertificate, DeathCertificate, BurialPermit, BirthCertificateUpdateRequest, DeathCertificateUpdateRequest

class BirthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True,},
            'description': {'required': False},
            'birth_number': {'read_only': True},
            'wilaya':{'read_only':True},
            'commune':{'read_only':True},
        }
        read_only_fields = ['user','hospital','id']


class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecord
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False},
            'age': {'read_only': True},
            'death_number': {'read_only': True},
            'death_wilaya':{'read_only':True},
            'death_commune':{'read_only':True},
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
    

class StatisticSerializer(serializers.Serializer):
    death = serializers.IntegerField()
    birth = serializers.IntegerField()
    total = serializers.IntegerField()


class PublicDeathCertificateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mother_name = serializers.CharField()
    father_name = serializers.CharField()
    birth_date = serializers.DateField()
    death_date = serializers.DateField()
    death_number = serializers.CharField()
    death_wilaya = serializers.CharField()

class PublicBirthCertificateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mother_name = serializers.CharField()
    father_name = serializers.CharField()
    birth_date = serializers.DateField()
    birth_number = serializers.CharField()
    birth_wilaya = serializers.CharField()


class BirthCertificateUpdateRequestSerializer(serializers.ModelSerializer):
    original_certificate= BirthCertificateSerializer(source='certificate')

    class Meta:
        model = BirthCertificateUpdateRequest
        fields = '__all__'
        read_only_fields = ['user','id','original_certificate','updat_data','court']
    
class DeathCertificateUpdateRequestSerializer(serializers.ModelSerializer):
    original_certificate= DeathCertificateSerializer(source='certificate')

    class Meta:
        model = DeathCertificateUpdateRequest
        fields = '__all__'
        read_only_fields = ['user','id','original_certificate','updat_data','court']
    
class BurialPermitSerializer(serializers.ModelSerializer):
    death_Certificate = DeathCertificateSerializer(source='certificate')
    death_record = DeathRecordSerializer(source='record')
    class Meta:
        model = BurialPermit
        fields = '__all__'
        read_only_fields = ['user','id','certificate','death_Certificate','record','death_record']