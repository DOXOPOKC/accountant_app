from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
