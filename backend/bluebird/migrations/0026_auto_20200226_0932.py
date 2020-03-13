# Generated by Django 3.0.3 on 2020-02-26 09:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0025_auto_20200217_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentspackage',
            name='price_count',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Расчет стоимости'),
        ),
        migrations.AlterField(
            model_name='contragent',
            name='current_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Конечная дата оказания услуг'),
        ),
        migrations.AlterField(
            model_name='normative',
            name='value',
            field=models.FloatField(blank=True, null=True, verbose_name='Значение норматива (год.)'),
        ),
        migrations.AlterField(
            model_name='signuser',
            name='tel_number',
            field=models.CharField(default='', max_length=255, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='signuser',
            name='city',
            field=models.CharField(default='Кемерово', max_length=255, verbose_name='Город/населенный пункт'),
        ),
    ]
