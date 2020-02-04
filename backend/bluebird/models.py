import datetime
import uuid
import os

from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


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
                                    auto_now_add=True, blank=True,
                                    null=True)
    number_contract = models.OneToOneField('ContractNumberClass',
                                           on_delete=models.CASCADE,
                                           max_length=255,
                                           blank=True, null=True)
    current_contract_date = models.DateField('Дата заключения договора',
                                             blank=True, null=True)
    signed_user = models.ForeignKey(User, blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='signed')
    current_user = models.ForeignKey(User, blank=True, null=True,
                                     on_delete=models.CASCADE,
                                     related_name='current')
    platform = models.IntegerField('№ площадки',
                                   blank=True, null=True)

    def create_package_and_folder(self):
        self.check_and_create_parent_folder()
        if not os.path.isdir(self.get_str_as_path()):
            os.mkdir(self.get_str_as_path(), mode=0o777)
        # package = DocumentsPackage.objects.get_or_create(contragent=self,
        #                                                  is_active=True)
        # package = DocumentsPackage.objects.create(contragent=self)
        # package.initialize_sub_folders()

    def check_and_create_parent_folder(self):
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,
                                          KLASS_TYPES[self.klass][1])):
            os.mkdir(os.path.join(settings.MEDIA_ROOT,
                     KLASS_TYPES[self.klass][1]), mode=0o777)

    def get_str_as_path(self):
        return os.path.join(os.path.join(settings.MEDIA_ROOT,
                                         KLASS_TYPES[self.klass][1]),
                            f'{self.pk} {self.excell_name}')


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

    class Meta:
        abstract = True


class ActFile(AbstractFileModel):
    act_unique_number = models.ForeignKey('ActUniqueNumber',
                                          on_delete=models.CASCADE,
                                          null=True, blank=True)

    class Meta:
        abstract = False

    @classmethod
    def initialize_folder(cls, path: str):
        if not os.path.isdir(f'{path}/акты/'):
            os.makedirs(f'{path}/акты/')

    @classmethod
    def get_files_path(cls, package: 'DocumentsPackage'):
        tmp_path = package.get_save_path()
        cls.initialize_folder(tmp_path)
        return os.path.join(tmp_path, 'акты/')


class CountFile(AbstractFileModel):
    count_unique_number = models.ForeignKey('CountUniqueNumber',
                                            on_delete=models.CASCADE,
                                            null=True, blank=True)

    class Meta:
        abstract = False

    @classmethod
    def initialize_folder(cls, path: str):
        if not os.path.isdir(f'{path}/счета/'):
            os.makedirs(f'{path}/счета/')

    @classmethod
    def get_files_path(cls, package: 'DocumentsPackage'):
        tmp_path = package.get_save_path()
        cls.initialize_folder(tmp_path)
        return os.path.join(tmp_path, 'счета/')


class CountFactFile(AbstractFileModel):
    count_fact_unique_number = models.ForeignKey('CountFactUniqueNumber',
                                                 on_delete=models.CASCADE,
                                                 null=True, blank=True)

    class Meta:
        abstract = False

    @classmethod
    def initialize_folder(cls, path: str):
        if not os.path.isdir(f'{path}/счета_фактуры/'):
            os.makedirs(f'{path}/счета_фактуры/')

    @classmethod
    def get_files_path(cls, package: 'DocumentsPackage'):
        tmp_path = package.get_save_path()
        cls.initialize_folder(tmp_path)
        return os.path.join(tmp_path, 'счета_фактуры/')


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
    name_uuid = models.CharField(max_length=255, default=uuid.uuid4,
                                 null=True, blank=True, editable=False)
    is_active = models.BooleanField('Активный пакет', default=True)
    creation_date = models.DateField('Дата создания пакета', auto_now_add=True)
    # Единичные документы
    contract = models.CharField('Договор', max_length=255,
                                null=True, blank=True)
    court_note = models.CharField('Претензия', max_length=255,
                                  null=True, blank=True)
    act_count = models.CharField('Акт сверки', max_length=255,
                                 null=True, blank=True)
    # Пакеты документов
    act_files = GenericRelation(ActFile)
    count_files = GenericRelation(CountFile)
    count_fact_files = GenericRelation(CountFactFile)
    files = GenericRelation(OtherFile)

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
    value = models.FloatField('Значение норматива (мес.)',
                              null=True, blank=True)

    def __str__(self):
        return (f'Норматив: {self.value}/мес.,'
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


class ActUniqueNumber(models.Model):
    number = models.CharField('Номер', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def set_number(self, number: str):
        self.number = number
        self.save(force_update=True)
        return self

    @classmethod
    def create(cls):
        cls_obj = cls.objects.create(number='')
        cls_obj.set_number(f'{cls_obj.pk:08}/01')
        return cls_obj


class CountUniqueNumber(models.Model):
    number = models.CharField('Номер', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def set_number(self, number: str):
        self.number = number
        self.save(force_update=True)
        return self

    @classmethod
    def create(cls):
        cls_obj = cls.objects.create(number='')
        cls_obj.set_number(f'{cls_obj.pk:08}/01')
        return cls_obj


class CountFactUniqueNumber(models.Model):
    number = models.CharField('Номер', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def set_number(self, number: str):
        self.number = number
        self.save(force_update=True)
        return self

    @classmethod
    def create(cls):
        cls_obj = cls.objects.create(number='')
        cls_obj.set_number(f'{cls_obj.pk:08}/01')
        return cls_obj
