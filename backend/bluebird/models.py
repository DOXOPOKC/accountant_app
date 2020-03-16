import datetime
import uuid
import os

from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User

from django.conf import settings
from django.db import models

from .snippets import str_add_app
from bluebird.templatetags.template_extra_filters import plur_form


KLASS_TYPES = [
        (0, 'Пусто'),
        (1, 'Юридическое лицо без договора'),
        (2, 'Юридическое лицо с договором'),
        (3, 'ИЖС без договора'),
        (4, 'ИЖС с договором'),
        (5, 'Физическое лицо'),
    ]

NORM_TYPE = [
    (0, '1 м2 общей площади'),
    (1, '1 место'),
    (2, '1 человек'),
]

DOC_TYPE = [
    (0, 'Доверенность'),
    (1, 'Пасспорт'),
]

POST_TYPE = [
    (0, 'Клиент-менеджер'),
    (1, 'Старший менеджер по работе с ЮЛ'),
    (2, 'Менеджер'),
]


class Contragent(models.Model):
    """
    Класс Контрагента.

    """
    klass = models.IntegerField('Класс контрагента',
                                choices=KLASS_TYPES,
                                default=0)
    excell_name = models.CharField('Наименование контрагента (из Excell)',
                                   max_length=255)
    dadata_name = models.CharField('Наименование контрагента (из Dadata)',
                                   max_length=255, blank=True, null=True)
    debt = models.FloatField('Сумма задолжности', default=0.00)
    inn = models.BigIntegerField('ИНН контрагента', blank=True, null=True)
    ogrn = models.BigIntegerField('ОГРН контрагента', blank=True, null=True)
    kpp = models.BigIntegerField('КПП контрагента', blank=True, null=True)

    rs = models.CharField('Р/с', max_length=255, blank=True, null=True)
    ks = models.CharField('К/с', max_length=255, blank=True, null=True)
    bank = models.CharField('Наименование банка', max_length=255, blank=True,
                            null=True)
    bik = models.CharField('БИК', max_length=255, blank=True, null=True)
    opf = models.CharField('ОПФ', max_length=255, blank=True, null=True)

    director_status = models.CharField('Директор (физ. лицо либо юр. лицо)',
                                       max_length=255, blank=True, null=True)
    director_name = models.CharField('Имя либо иное наименование директора',
                                     max_length=255, blank=True, null=True)
    creation_date = models.DateField('Дата создания контрагента (юл)',
                                     blank=True, null=True)
    is_func = models.BooleanField('Признак активности контрагента',
                                  default=True)
    okved = models.CharField('ОКВЭД',
                             max_length=255, blank=True, null=True)
    physical_address = models.CharField('Физический адресс',
                                        max_length=255)
    legal_address = models.CharField('Юридический адресс',
                                     max_length=255, blank=True, null=True)
    # TODO СВЯЗАТЬ НОРМАТИВ И ОКВЭД?
    norm_value = models.ForeignKey('NormativeCategory',
                                   related_name='normatives',
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)
    stat_value = models.FloatField('Показатель', blank=True, null=True)
    contract_accept_date = models.DateField(
                            'Дата начала оказания услуг',
                            default=datetime.date.fromisoformat('2018-07-01'),
                            blank=True, null=True
                    )
    current_date = models.DateField('Конечная дата оказания услуг',
                                    default=datetime.date.today, blank=True,
                                    null=True)
    number_contract = models.OneToOneField('ContractNumberClass',
                                           on_delete=models.CASCADE,
                                           max_length=255,
                                           blank=True, null=True)
    current_contract_date = models.DateField('Дата заключения договора',
                                             blank=True, null=True)
    signed_user = models.ForeignKey('SignUser', blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='signed')
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                     null=True, on_delete=models.CASCADE,
                                     related_name='current')
    platform = models.IntegerField('№ площадки',
                                   blank=True, null=True)

    def create_package_and_folder(self):
        self.check_and_create_parent_folder()
        if not os.path.isdir(self.get_str_as_path()):
            os.mkdir(self.get_str_as_path(), mode=0o777)

    def check_and_create_parent_folder(self):
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,
                                          KLASS_TYPES[self.klass][1])):
            os.mkdir(os.path.join(settings.MEDIA_ROOT,
                     KLASS_TYPES[self.klass][1]), mode=0o777)

    def get_str_as_path(self):
        return os.path.join(os.path.join(settings.MEDIA_ROOT,
                                         KLASS_TYPES[self.klass][1]),
                            f'{self.pk} {self.excell_name}')

    def __str__(self):
        return f'{self.excell_name}'


class SignUser(models.Model):
    name = models.CharField('ФИО отвественного лица', max_length=255)
    document = models.IntegerField('Документ основания', choices=DOC_TYPE,
                                   default=0)
    position = models.IntegerField('Должность', choices=POST_TYPE,
                                   default=0)
    doc_number = models.CharField('Номер документа', max_length=255)
    doc_date = models.DateField('Дата начала действия документа')
    address = models.CharField('Адресс', max_length=255)
    city = models.ForeignKey('CityModel', on_delete=models.CASCADE,
                             blank=True, null=True)
    tel_number = models.CharField('Телефон', max_length=255, default='')

    def __str__(self):
        return self.name


class AbstractFileModel(models.Model):
    file_name = models.CharField('Название файла', max_length=255,
                                 null=True, blank=True)
    file_path = models.CharField('Путь', max_length=255, blank=True, null=True)
    creation_date = models.DateField('Дата создания файла',
                                     blank=True, null=True)

    # Подгрузка произвольного количества файлов
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file_type = models.ForeignKey('DocumentTypeModel',
                                  on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(str_add_app(self.file_path)):
            os.remove(str_add_app(self.file_path))
        return super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        abstract = True


class SingleFile(AbstractFileModel):

    def __str__(self):
        return str(self.file_type)


class PackFile(AbstractFileModel):
    unique_number = models.ForeignKey('SyncUniqueNumber',
                                      on_delete=models.CASCADE,
                                      null=True, blank=True)

    class Meta:
        abstract = False

    def initialize_folder(self, path: str):
        if self.file_type:
            tmp_str_path = plur_form(self.file_type.doc_type)
            if not os.path.isdir(f'{path}/{tmp_str_path}/'):
                os.makedirs(f'{path}/{tmp_str_path}/')
        else:
            raise AttributeError()

    def get_files_path(self, package: 'DocumentsPackage'):
        tmp_path = package.get_save_path()
        self.initialize_folder(tmp_path)
        return os.path.join(tmp_path, f'{plur_form(self.file_type.doc_type)}/')


def other_files_directory_path(instance, filename):
    p = instance.content_object.get_save_path()
    return '{0}/прочие/{1}'.format(p, filename)


class OtherFile(AbstractFileModel):
    file_obj = models.FileField('Произвольные файлы',
                                upload_to=other_files_directory_path,
                                max_length=500)


class DocumentsPackage(models.Model):
    """ Модель пакета документов.
    act_files -  Акты
    count_files - Счета
    count_fact_files - Счета фактуры
    files - Произвольные файлы
    """
    contragent = models.ForeignKey(Contragent, on_delete=models.CASCADE,
                                   related_name='contragents',
                                   related_query_name='contragent',
                                   null=True, blank=True)
    name_uuid = models.CharField('Идентификатор пакета', max_length=255,
                                 default=uuid.uuid4, null=True, blank=True,
                                 editable=False)
    is_active = models.BooleanField('Активный пакет', default=True)
    creation_date = models.DateField('Дата создания пакета', auto_now_add=True)

    single_files = GenericRelation(SingleFile)

    pack_files = GenericRelation(PackFile)

    other_files = GenericRelation(OtherFile)


    def __str__(self):
        return f'Пакет {self.name_uuid}'

    def get_save_path(self):
        if self.contragent:
            return os.path.join(self.contragent.get_str_as_path(),
                                str(self.name_uuid))
        else:
            return f'{self.name_uuid}'

    @classmethod
    def get_active_package(cls, contragent: Contragent):
        res = cls.objects.get(contragent__id=contragent.pk, is_active=True)
        return res

    def initialize_sub_folders(self):
        os.makedirs(str(self.get_save_path()), exist_ok=True)


class SingleFilesTemplate(models.Model):
    contagent_type = models.IntegerField(choices=KLASS_TYPES, default=0)
    documents = models.ManyToManyField('DocumentTypeModel',
                                       related_name='document_type')

#     def clean(self):
#         for doc in self.documents:
#             if doc.is_pack:
#                 raise ValidationError('There is pack documents type included.\
# Remove them')

#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)


class PackFilesTemplate(models.Model):
    contagent_type = models.IntegerField(choices=KLASS_TYPES, default=0)
    documents = models.ManyToManyField('DocumentTypeModel',
                                       related_name='document_type_pack')


class NormativeCategory(models.Model):
    """ Класс Категории норматива """
    name = models.CharField('Вид объекта',
                            max_length=255)
    norm_type = models.IntegerField('Показатель расчета', default=0,
                                    choices=NORM_TYPE, blank=True, null=True)
    normative = models.ManyToManyField('Normative', related_name='normatives',
                                       verbose_name='Нормативы')

    def __str__(self):
        return self.name

    @property
    def print_norm_type(self):
        return NORM_TYPE[self.norm_type][1]


class Normative(models.Model):
    """ Класс норматива """
    since_date = models.DateField('Дата начала действия норматива',
                                  null=True, blank=True)
    up_to_date = models.DateField('Дата окончания действия норматива',
                                  null=True, blank=True)
    value = models.FloatField('Значение норматива (год.)',
                              null=True, blank=True)

    def __str__(self):
        return (f'Норматив: {self.value}/год.,'
                + f' действующий с {self.since_date.strftime("%d.%m.%Y")}'
                + f' по {self.up_to_date.strftime("%d.%m.%Y")}')


class Contract(models.Model):
    """ Класс контракта. Нужен что бы получать уникальный номер контракта.
    Сохраняет дату когда был создан, для корректной генерации строкового
    представления.
    """
    date_field = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk:06}-{(self.date_field).year}/ТКО/01'


class ContractNumberClass(models.Model):
    """ Модель класса прокси для соединения класса документа и контрагента.

    Принимает на вход необязательные параметры:
        new - определяем, надо генерировать новый номер или есть
                старый. Булево значение. True = генерируем;
        exist_number - существующий номер договора. Строка;

    У класса есть такие поля как:
        is_generated - хранит булево значение. Определяет был ли сгенерирован
                        номер или взят из внешних источников;
        contract_obj - объект модели самого номера контракта;
        contract_exist_number - существующий номер контракта. Пустая строка,
                                если мы сгенерировали новый номер;
        contract_number - возвращает строковое представление номера, независимо
                            от того, сгенерирован код или получен из внешнего
                            источника.
    """
    is_generated = models.BooleanField(default=False)
    contract_obj = models.OneToOneField(Contract,
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)
    contract_exist_number = models.CharField(default='',
                                             max_length=255,
                                             null=True, blank=True)

    @classmethod
    def create(cls, new: bool = False, exist_number: str = ''):
        contract_num_obj = cls(is_generated=new)
        if new:
            contract_num_obj.contract_obj = Contract.objects.create()
        else:
            contract_num_obj.contract_exist_number = exist_number
        contract_num_obj.save()
        return contract_num_obj

    @property
    def contract_number(self):
        if self.is_generated:
            return str(self.contract_obj)
        else:
            return self.contract_exist_number

    def __str__(self):
        return self.contract_number


class SyncUniqueNumber(models.Model):

    def __str__(self):
        return f'{self.pk:08}/01'


class CityModel(models.Model):
    name = models.CharField('Город', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class TemplateModel(models.Model):
    template_path = models.CharField('Путь до шаблона', max_length=255)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    contragent_type = models.IntegerField('Тип контрагента',
                                          choices=KLASS_TYPES, default=0)
    document_type = models.ForeignKey('DocumentTypeModel',
                                      verbose_name='Тип документа',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.document_type)}|\
{KLASS_TYPES[self.contragent_type][1]}|{self.city}'


class DocumentTypeModel(models.Model):
    doc_type = models.CharField('Тип документа', max_length=255,
                                null=True, blank=True)
    is_pack = models.BooleanField('Пакет документов', default=False)

    def __str__(self):
        return self.doc_type
