# Generated by Django 3.0.7 on 2020-07-27 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0012_auto_20200724_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='actexam',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название файла'),
        ),
    ]