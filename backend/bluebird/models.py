import datetime

from django.contrib.auth.models import User
from django.db import models


KLASS_TYPES = [
        (0, 'Пусто'),
        (1, 'Юридическое лицо без договора'),
        (2, 'Юридическое лицо с договором'),
        (3, 'ИЖС без договора'),
        (4, 'ИЖС с договором'),
        (5, 'Физическое лицо'),
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
    debt = models.FloatField('Сумма задолжности',
                             default=0.00)
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
                            'Дата заключения договора',
                            default=datetime.date.fromisoformat('2018-07-01'),
                            blank=True, null=True
                    )
    current_date = models.DateField('Текущая дата',
                                    auto_now_add=True, blank=True,
                                    null=True)
    number_contract = models.OneToOneField('ContractNumberClass',
                                           on_delete=models.CASCADE,
                                           max_length=255,
                                           blank=True, null=True)
    current_contract_date = models.DateTimeField('Дата заключения договора',
                                                 blank=True, null=True)
    signed_user = models.ForeignKey(User, blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='signed')
    current_user = models.ForeignKey(User, blank=True, null=True,
                                     on_delete=models.CASCADE,
                                     related_name='current')
    platform = models.IntegerField('№ площадки',
                                   blank=True, null=True)


class NormativeCategory(models.Model):
    """ Класс Категории норматива """
    name = models.CharField('Вид объекта',
                            max_length=255)
    normative = models.ManyToManyField('Normative', related_name='normatives',
                                       verbose_name='Нормативы')

    def __str__(self):
        return self.name


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


class DocumentUniqueNumber(models.Model):
    """ Модель номера документа. Уникальный номер для произвольного документа
    (не договора)."""
    def __str__(self):
        return f'{self.pk:05}/1'


class DocumentUniqueNumberGenerator(models.Model):
    """ Модель прокси для соединения уникального номера и контрагента.
    Необходима для сохранения отношений, т.к. возможно понадобится
    перегенерировать документы."""
    date_when = models.DateField(null=True, blank=True)
    contragent = models.ForeignKey(Contragent, on_delete=models.CASCADE,
                                   blank=True, null=True)
    unique_number = models.OneToOneField(DocumentUniqueNumber,
                                         on_delete=models.CASCADE)

    @classmethod
    def create(cls, date_when, contragent: Contragent):
        unique_n = DocumentUniqueNumber.objects.create()
        return cls.objects.create(date_when=date_when,
                                  contragent=contragent,
                                  unique_number=unique_n)

    def __str__(self):
        return str(self.unique_number)
