# Generated by Django 3.0.2 on 2020-01-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0003_contragent_klass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contragent',
            name='is_func',
            field=models.BooleanField(default=True),
        ),
    ]
