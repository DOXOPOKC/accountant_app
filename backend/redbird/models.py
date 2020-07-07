from django.db import models
from django.conf import settings

from bluebird.models import DocumentsPackage, State


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
