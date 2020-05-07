from rest_framework import serializers
from .models import (Contragent, DocumentsPackage, OtherFile, PackFile,
                     NormativeCategory, SignUser,
                     DocumentTypeModel, SingleFile, PackFilesTemplate, State,
                     Event, Commentary)

from django_q.models import Task
from django.core.exceptions import ObjectDoesNotExist


class ContragentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contragent
        fields = ['id', 'klass', 'excell_name',
                  'inn', 'debt', 'physical_address', ]


class PackageShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsPackage
        fields = ['id', 'name_uuid', 'contragent', 'is_active',
                  'creation_date', 'package_state_date', 'package_state', ]


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
        fields = ['id', 'file_name', 'file_path', 'file_type',
                  'creation_date', ]


class PackFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackFile
        fields = ['id', 'file_name', 'file_path', 'file_type',
                  'creation_date', ]


class OtherFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherFile
        fields = ['id', 'file_name', 'file_path', 'file_type',
                  'creation_date', ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        events = EventSerializer(obj.get_linked_events(), many=True).data
        if len(events):
            return events
        return dict()

    class Meta:
        model = State
        fields = ['id', 'name_state', 'departments', 'is_initial_state',
                  'is_final_state', 'events', ]


class PackageFullSerializer(serializers.ModelSerializer):
    package_state = StateSerializer(many=False)
    single_files = SingleFileSerializer(many=True)
    pack_files = serializers.SerializerMethodField()
    other_files = OtherFileSerializer(many=True)

    def get_pack_files(self, obj):
        contragent = obj.contragent
        try:
            pack_template = PackFilesTemplate.objects.get(
                                            contagent_type=contragent.klass)

            docs = PackFile.objects.filter(object_id=obj.id)
            tmp_templ_dict = dict()
            tmp_template_doc_types_list = pack_template.documents.all()
            for tmpl in tmp_template_doc_types_list:
                tmp_templ_dict[str(tmpl)] = PackFileListSerializer(
                    list(docs.filter(file_type=tmpl)), many=True).data
            return tmp_templ_dict
        except ObjectDoesNotExist:
            return dict()

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
        fields = ['id', 'name', 'position', 'address', ]


class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormativeCategory
        fields = ['id', 'name', ]


class CommentarySerializer(serializers.ModelSerializer):

    # content_object = serializers.SerializerMethodField()

    # def get_content_object(self, value):
    #     if isinstance(value, DocumentsPackage):
    #         return 'package_id: ' + value.id
    #     raise Exception('Unexpected type of tagged object')

    class Meta:
        model = Commentary
        fields = ['id', 'commentary_text', 'creation_date', ]
