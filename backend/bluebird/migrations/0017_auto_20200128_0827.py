# Generated by Django 3.0.2 on 2020-01-28 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0016_auto_20200128_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentspackage',
            name='contragent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contragents', related_query_name='contragent', to='bluebird.Contragent'),
        ),
    ]
