# Generated by Django 3.0.2 on 2020-01-28 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0015_auto_20200128_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentspackage',
            name='act_count',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Акт сверки'),
        ),
    ]