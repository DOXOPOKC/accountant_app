# Generated by Django 3.0.2 on 2020-01-31 03:12

import bluebird.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0022_auto_20200130_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherfile',
            name='file_obj',
            field=models.FileField(max_length=500, upload_to=bluebird.models.other_files_directory_path, verbose_name='Произвольные файлы'),
        ),
    ]
