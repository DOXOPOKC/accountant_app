from rest_framework import serializers
from .models import (Contragent, DocumentsPackage, OtherFile)

from django_q.models import Task


class ContragentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = ['id', 'klass', 'excell_name',
                  'inn', 'debt', 'physical_address']


class PackageShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsPackage
        fields = ['id', 'name_uuid', 'contragent', 'is_active',
                  'creation_date']


class ContragentFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = '__all__'
        extra_kwargs = {'klass': {'required': False},
                        'excell_name': {'required': False},
                        'inn': {'required': False},
                        'debt': {'required': False},
                        'physical_address': {'required': False},
                        'ogrn': {'required': False},
                        'kpp': {'required': False},
                        }


class PackageFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# class OtherFileListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OtherFile
#         fields = '__all__'


class OtherFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherFile
        fields = '__all__'
