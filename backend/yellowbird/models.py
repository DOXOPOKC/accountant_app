from django.db import models
from django.contrib.auth.models import AbstractUser

from bluebird.models import STRATEGIES_TUPLES


class User(AbstractUser):
    username = models.CharField("Логин", max_length=255, unique=True)
    password = models.CharField("Пароль", max_length=255)
    name = models.CharField("Имя", max_length=255, blank=True, null=True)
    last_name = models.CharField("Фамилия", max_length=255, blank=True,
                                 null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE,
                                   blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


class Department(models.Model):
    title = models.CharField('Отдел', max_length=255, unique=True)
    strategy = models.IntegerField('Стратегия отсеивания результатов',
                                   choices=STRATEGIES_TUPLES, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Отделы'
