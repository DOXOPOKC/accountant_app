from rest_framework import serializers
from .models import (Contragent, DocumentsPackage, OtherFile, ActFile,
                     CountFile, CountFactFile, NormativeCategory, SignUser,
                     DocumentTypeModel, SingleFile)

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


class DocumentTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypeModel
        fields = ['doc_type', ]


class SingleFileSerializer(serializers.ModelSerializer):
    file_type = DocumentTypeModelSerializer()

    class Meta:
        model = SingleFile
        fields = ['file_name', 'file_path', 'file_type']


class ActFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActFile
        fields = '__all__'


class CountFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountFile
        fields = '__all__'


class CountFactFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountFactFile
        fields = '__all__'


class OtherFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherFile
        fields = '__all__'


class PackageFullSerializer(serializers.ModelSerializer):
    single_files = SingleFileSerializer(many=True)
    act_files = ActFileListSerializer(many=True)
    count_files = CountFileListSerializer(many=True)
    count_fact_files = CountFactFileListSerializer(many=True)
    other_files = OtherFileSerializer(many=True)

    class Meta:
        model = DocumentsPackage
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SignUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUser
        fields = ['id', 'name', 'position', 'address']


class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormativeCategory
        fields = ['id', 'name']
