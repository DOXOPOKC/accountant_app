# Generated by Django 3.0.2 on 2020-01-29 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0018_auto_20200128_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='actfile',
            name='number_obj',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.ActUNGen'),
        ),
    ]
