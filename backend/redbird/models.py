from django.db import models
from django.conf import settings

from bluebird.models import DocumentsPackage, State
from yellowbird.models import Department
from .agregators import AGREGATORS_LIST


class JournalRecord(models.Model):
    journal = models.ForeignKey('Journal',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    state = models.ForeignKey(State,
                              on_delete=models.CASCADE)
    date = models.DateField('Дата', auto_now=True)


class Journal(models.Model):
    pack = models.ForeignKey(DocumentsPackage, on_delete=models.CASCADE)

    def add_record(self, user):
        record = JournalRecord.objects.create(
            journal=self, user=user, state=self.pack.package_state
        )
        return record


class Report(models.Model):
    name = models.CharField(verbose_name='Название отчета', max_length=255)
    departments = models.ManyToManyField(Department, blank=True, null=True)
    template = models.ForeignKey('ReportTemplate', on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   null=True)

    def get_report(self):
        pass


class ReportTemplate(models.Model):
    name = models.CharField(verbose_name='Название шаблона отчета',
                            max_length=255)
    file_path = models.FileField(verbose_name="Template file")
    data_set = models.ManyToManyField("DataPart")

    def get_params(self):
        result = list()
        for data in self.data_set.all():
            result.append(data.get_rarams())
        return result

    def gather_data(self):
        pass

    def return_result(self):
        pass


class DataPart(models.Model):
    agregator = models.IntegerField(unique=True, choices=AGREGATORS_LIST,
                                    default=0)

    def get_rarams(self):
        return AGREGATORS_LIST[self.agregator][1].get_params()
