import datetime
import os
import uuid
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from bluebird.templatetags.template_extra_filters import (plur_form,
proper_last_name)
from bluebird.tasks import calc_create_gen_async

from django_q.tasks import async_task

from .snippets import str_add_app, KLASS_TYPES, DOC_TYPE


NORM_TYPE = [
    (0, '1 м2 общей площади'),
    (1, '1 место'),
    (2, '1 человек'),
]


POST_TYPE = [
    (0, 'Клиент-менеджер'),
    (1, 'Старший менеджер по работе с ЮЛ'),
    (2, 'Менеджер'),
]


class Adress(models.Model):
    state = models.CharField(verbose_name="Область", max_length=255)
    city = models.CharField(verbose_name="Город", max_length=255)
    street = models.CharField(verbose_name="Улица", max_length=255)
    block = models.CharField(verbose_name="Номер дома", max_length=10)


class ContragentClass(models.Model):
    name = models.CharField('Наименование', max_length=255)


class Contragent(models.Model):
    """
    Класс Контрагента.

    """
    # klass = models.ForeignKey(ContragentClass, on_delete=models.CASCADE)
    klass = models.IntegerField(choices=KLASS_TYPES, default=0)
    excell_name = models.CharField('Наименование контрагента (из Excell)',
                                   max_length=255)
    dadata_name = models.CharField('Наименование контрагента (из Dadata)',
                                   max_length=255, blank=True, null=True)
    debt = models.FloatField('Сумма задолжности', default=0.00)
    debt_period = models.IntegerField('Количество неоплаченных периодов, мес.',
                                      blank=True, null=True)
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

    #  TODO REWORK THIS AREA
    physical_address = models.CharField('Физический адресс',
                                        max_length=255)
    legal_address = models.CharField('Юридический адресс',
                                     max_length=255, blank=True, null=True)
    #  END OF REWORK

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

    platform = models.IntegerField('№ площадки',
                                   blank=True, null=True)

    judge_link = models.CharField(verbose_name="", max_length=255,
                                  blank=True, null=True)
    fss_link = models.CharField(verbose_name="", max_length=255,
                                blank=True, null=True)

    personal_number = models.CharField(verbose_name="Лицевой счет",
                                       max_length=255, blank=True, null=True)

    passport_number = models.CharField(verbose_name="Номер паспорта",
                                       max_length=15, blank=True, null=True)
    passport_date = models.DateField(verbose_name="Дата выдачи пасспорта",
                                     blank=True, null=True)
    passport_origin = models.CharField(verbose_name="Кем выдан пасспорт",
                                       max_length=15, blank=True, null=True)
    snils = models.CharField(verbose_name="СНИЛС",
                             max_length=15, blank=True, null=True)

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

    @property
    def current_user(self):
        package = self.get_active_package()
        if package:
            res = [user for user in package.package_users.all(
                ) if package.package_state.is_permitted(user)]
            return res
        return None

    @current_user.setter
    def current_user(self, user):
        package = self.get_active_package()
        if package and not package.is_user_in_package(user, True):
            package.package_users.add(user)
            package.save()

    @property
    def active_package(self):
        return self.get_active_package()

    def get_all_packages(self):
        return DocumentsPackage.objects.filter(contragent=self.pk) or None

    def get_active_package(self):
        res = DocumentsPackage.get_active_package(self)
        return res

    def reset_debt(self):
        self.debt = 0
        self.debt_period = 0
        self.save()

    def __str__(self):
        return f'{self.excell_name}'

    class Meta:
        verbose_name_plural = "Контрагенты"


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
    sign = models.ImageField('Подпись', upload_to='signs/',
                             blank=True, null=True)

    def __str__(self):
        # return self.name
        return f"{proper_last_name(self.name)}, {POST_TYPE[self.position][1]}"

    def save(self, *args, **kwargs):
        instance = SignUser.objects.get(id=self.id)
        if self.sign != instance.sign and instance.sign:
            if os.path.exists(instance.sign.url):
                os.remove(instance.sign.url)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Отвественные лица с правом подписи"


class Commentary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    commentary_text = models.TextField('Комментарий', blank=True, null=True)
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


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

    class Meta:
        verbose_name_plural = "Единичные файлы"


class PackFile(AbstractFileModel):
    unique_number = models.ForeignKey('SyncUniqueNumber',
                                      on_delete=models.CASCADE,
                                      null=True, blank=True)

    class Meta:
        abstract = False
        verbose_name_plural = "Фаилы набора"

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

    commentary = GenericRelation(Commentary, related_query_name='file')

    class Meta:
        verbose_name_plural = "Прочие файлы"


class ActExam(models.Model):
    FOLDER = 'Акт осмотра/'

    file_path = models.CharField('Путь', max_length=255, blank=True, null=True)
    file_name = models.CharField('Название файла', max_length=255,
                                 null=True, blank=True)

    @classmethod
    def initialize_folder(cls, path: str):
        tmp_path = f'{path}/{cls.FOLDER}'
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)

    @classmethod
    def get_files_path(cls, package: 'DocumentsPackage'):
        tmp_path = package.get_save_path()
        ActExam.initialize_folder(tmp_path)
        return os.path.join(tmp_path, cls.FOLDER)

    def clear_file(self):
        if os.path.exists(str_add_app(self.file_path)):
            os.remove(str_add_app(self.file_path))
            self.file_path = None
            self.file_name = None
            self.save()

    def delete(self, using=None, keep_parents=False):
        self.clear_file()
        return super().delete(using=using, keep_parents=keep_parents)


class DocumentsPackage(models.Model):
    """ Модель пакета документов.
    contragent - ID контрагента
    name_uuid - Уникальный ID пакета (каждый раз новый)
    is_active - Является ли пакет активным. Если True, то пакет в работе. Если
                False, то пакет закрыт.
    is_automatic - Создан ли пакет автоматически или пользователь может
                   редактировать наборы файлов и некоторые характеристики. Если
                   True, то нельзя подгружать свои договора и редактировать
                   debt_plan. Если False, то редактирование возможно.
    creation_date - Дата создания пакета.
    debt_plan - Сумма долга. Если is_automatic == True, то значение не
                редактируется. Если is_automatic == False, то значение
                необходимо заполнить.
    debt_fact - Сумма долга по факту. Заполняется при сторнировании или оплате.
    tax_count - Госпошлина. Можно заполнять в любом случае.
    package_users - Все пользователи пакета, работавшие с ним.
    package_state - Состояние пакета.
    package_state_date - Дата изменения состояния пакета.
    single_files -  Пакет одиночных документов. 
    pack_files - Пакет наборов файлов.
    other_files - Произвольные файлы.
    commentary - Комментарии.
    """
    contragent = models.ForeignKey(Contragent, on_delete=models.CASCADE,
                                   related_name='contragents',
                                   related_query_name='contragent',
                                   null=True, blank=True)
    name_uuid = models.CharField('Идентификатор пакета', max_length=255,
                                 default=uuid.uuid4, null=True, blank=True,
                                 editable=False)
    is_active = models.BooleanField('Активный пакет', default=True)
    is_automatic = models.BooleanField('Создан автоматически', default=True)
    creation_date = models.DateField('Дата создания пакета', auto_now_add=True)

    debt_plan = models.FloatField('Сумма задолжности (плановая)',
                                  default=0.00)
    debt_fact = models.FloatField('Сумма задолжности (фактическая)',
                                  default=0.00)
    tax_count = models.FloatField('Госпошлина', default=0.00)

    package_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name='packages')

    package_state = models.ForeignKey('State', on_delete=models.CASCADE,
                                      null=True, blank=True)

    package_state_date = models.DateField('Дата последнего действия',
                                          null=True, blank=True)

    single_files = GenericRelation(SingleFile)

    pack_files = GenericRelation(PackFile)

    other_files = GenericRelation(OtherFile)

    commentary = GenericRelation(Commentary, related_query_name='package')
    
    act = models.ForeignKey(ActExam, on_delete=models.CASCADE,
                            null=True, blank=True)

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
        try:
            res = cls.objects.get(contragent__id=contragent.pk, is_active=True)
            return res
        except ObjectDoesNotExist:
            return None

    def initialize_sub_folders(self):
        os.makedirs(str(self.get_save_path()), exist_ok=True)

    def is_user_in_package(self, user, use_department=False):
        users = self.package_users.all()
        if use_department:
            depts = [tmp_user.department for tmp_user in users]
            return (user.department in depts) or (user in users)
        return user in users

    def set_inactive(self):
        self.is_active = False
        self.save()

    def change_state_to(self, new_state, is_backward):
        self.package_state = new_state
        self.package_state_date = datetime.date.today()
        if not is_backward:
            async_task(calc_create_gen_async, self.contragent, self, False,
                       group=self.name_uuid)
        # TODO Journal log here!
        self.save()

    class Meta:
        verbose_name_plural = "Пакеты документов"


class DocumentStateEntity(models.Model):
    documents = models.ManyToManyField('DocumentTypeModel',
                                       related_name='document_type')
    states = models.ForeignKey('State', related_name='states',
                               on_delete=models.CASCADE,
                               blank=True, null=True)
    template = models.ForeignKey('DocumentFileTemplate',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)


class DocumentFileTemplate(models.Model):
    contagent_type = models.IntegerField(choices=KLASS_TYPES, default=0)
    is_package = models.BooleanField('Набор файлов', default=False)

    def __str__(self):
        return KLASS_TYPES[self.contagent_type][1]

    class Meta:
        verbose_name_plural = "Шаблоны файлов"

# class SingleFilesTemplate(models.Model):
#     contagent_type = models.IntegerField(choices=KLASS_TYPES, default=0)

#     def __str__(self):
#         return KLASS_TYPES[self.contagent_type][1]

#     class Meta:
#         verbose_name_plural = "Шаблоны единичных файлов"


# class PackFilesTemplate(models.Model):
#     contagent_type = models.IntegerField(choices=KLASS_TYPES, default=0)
#     documents = models.ManyToManyField('DocumentTypeModel',
#                                        related_name='document_type_pack')

#     def __str__(self):
#         return KLASS_TYPES[self.contagent_type][1]

#     class Meta:
#         verbose_name_plural = "Шаблоны наборов файлов"


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

    class Meta:
        verbose_name_plural = "Категории нормативов"


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

    class Meta:
        verbose_name_plural = "Нормативы"


class Contract(models.Model):
    """ Класс контракта. Нужен что бы получать уникальный номер контракта.
    Сохраняет дату когда был создан, для корректной генерации строкового
    представления.
    """
    date_field = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk:06}-{(self.date_field).year}/ТКО/01'

    class Meta:
        verbose_name_plural = "Сгенерированые номера договоров"


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

    class Meta:
        verbose_name_plural = "Номера договоров"


class SyncUniqueNumber(models.Model):

    def __str__(self):
        return f'{self.pk:08}/01'

    class Meta:
        verbose_name_plural = "Номера документов"


class CityModel(models.Model):
    name = models.CharField('Город', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Города"


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

    class Meta:
        verbose_name_plural = "Шаблоны документов"


class DocumentTypeModel(models.Model):
    doc_type = models.CharField('Тип документа', max_length=255,
                                null=True, blank=True)
    is_pack = models.BooleanField('Пакет документов', default=False)

    def __str__(self):
        return self.doc_type

    class Meta:
        verbose_name_plural = "Типы документов"


#########
# State #
#########

class State(models.Model):
    name_state = models.CharField('Состояние', max_length=255)
    departments = models.ManyToManyField('yellowbird.Department',
                                         verbose_name='Отделы',
                                         related_name='available_states')
    is_initial_state = models.BooleanField('Начальное состояние',
                                           default=False)
    is_final_state = models.BooleanField('Конечное состояние', default=False)

    def get_linked_events(self):
        return Event.objects.filter(from_state=self.id)

    def _is_dept_permitted(self, department):
        return department in self.departments.all()

    def is_permitted(self, user):
        return (user.is_superuser or user.is_staff
                or self._is_dept_permitted(user.department))

    def __str__(self):
        return self.name_state

    class Meta:
        verbose_name_plural = 'Состояния'


class Event(models.Model):
    name_event = models.CharField('Событие', max_length=255)
    from_state = models.ForeignKey(State, on_delete=models.CASCADE,
                                   verbose_name='Исходное состояние',
                                   blank=True, null=True,
                                   related_name='begin_states')
    to_state = models.ForeignKey(State, on_delete=models.CASCADE,
                                 verbose_name='Конечное состояние',
                                 blank=True, null=True,
                                 related_name='end_states')
    is_move_backward = models.BooleanField('Двигаемся обратно назад',
                                           default=False)

    def __str__(self):
        return self.name_event

    class Meta:
        verbose_name_plural = 'События'

##############
# Strategies #
##############


class ListStrategy(ABC):

    @abstractmethod
    def execute_list_strategy(self, user):
        raise NotImplementedError

    @abstractmethod
    def execute_single_strategy(self, pk, user):
        raise NotImplementedError


class OnlyEmptyRecords(ListStrategy):
    def execute_list_strategy(self, user):
        contragents = Contragent.objects.all()
        return [c for c in contragents if not c.active_package]

    def execute_single_strategy(self, pk, user):
        try:
            res = Contragent.objects.get(pk=pk)
            return res if (not res.active_package) else None
        except Contragent.DoesNotExist:
            return None


class OnlyMyRecordsStrategy(ListStrategy):

    def execute_list_strategy(self, user):
        contragents = Contragent.objects.filter(current_user__contain=user)
        return contragents

    def execute_single_strategy(self, pk, user):
        try:
            return Contragent.objects.get(pk=pk, current_user__contain=user)
        except Contragent.DoesNotExist:
            return None


class AllRecords(ListStrategy):
    def execute_list_strategy(self, user):
        contragents = Contragent.objects.all()
        return contragents

    def execute_single_strategy(self, pk, user):
        try:
            return Contragent.objects.get(pk=pk)
        except Contragent.DoesNotExist:
            return None


class AllInDepartmentRecords(ListStrategy):
    def execute_list_strategy(self, user):
        res = list()
        contragents = Contragent.objects.all()
        for c in contragents:
            tmp_pack = c.get_active_package()
            if tmp_pack:
                tmp_state = tmp_pack.package_state
                if tmp_state:
                    if tmp_state.is_permitted(user.department):
                        res.append(c)
                else:
                    res.append(c)
            else:
                res.append(c)
        return res

    def execute_single_strategy(self, pk, user):
        try:
            contragent = Contragent.objects.get(pk=pk)
            tmp_pack = contragent.get_active_package()
            if tmp_pack:
                tmp_list = [c.department == user.department
                            for c in contragent.current_user]
                if any(tmp_list):
                    return contragent
                return None
            return contragent
        except Contragent.DoesNotExist:
            return None


class MyAndEmptyRecordsStrategy(ListStrategy):

    def execute_list_strategy(self, user):
        res = list()
        contragents = Contragent.objects.all()
        for c in contragents:
            tmp_pack = c.get_active_package()
            if tmp_pack:
                tmp_state = tmp_pack.package_state
                if tmp_state:
                    if tmp_state.is_permitted(user) and (
                                            user in c.current_user):
                        res.append(c)
                else:
                    res.append(c)
            else:
                res.append(c)
        return res

    def execute_single_strategy(self, pk, user):
        try:
            contragent = Contragent.objects.get(pk=pk)
            tmp_pack = contragent.get_active_package()
            if tmp_pack:
                tmp_state = tmp_pack.package_state
                if tmp_state:
                    if tmp_state.is_permitted(user) and (
                                            user in contragent.current_user):
                        return contragent
            return contragent
        except Contragent.DoesNotExist:
            return None


STRATEGIES_LIST = ['Мои записи и пустые', 'Все по отделу', 'Все',
                   'Только мои записи', 'Только пустые записи']

STRATEGIES_TUPLES = list(enumerate(STRATEGIES_LIST))

STRATEGIES_FUNCTIONS = [MyAndEmptyRecordsStrategy, AllInDepartmentRecords,
                        AllRecords, OnlyMyRecordsStrategy, OnlyEmptyRecords]

STRATEGIES = dict(zip(STRATEGIES_LIST, STRATEGIES_FUNCTIONS))

ZIP_FILES_ACTIONS = {
    0: "Скачать весь пакет",
    1: "Скачать основные файлы",
    2: "Скачать акты",
    3: "Скачать счета",
    4: "Скачать счета фактуры",
    5: "Скачать прочие файлы",
}
