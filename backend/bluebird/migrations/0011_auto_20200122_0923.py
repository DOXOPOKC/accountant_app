# Generated by Django 3.0.2 on 2020-01-22 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0010_auto_20200121_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActUN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActUNGen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_when', models.DateField(blank=True, null=True)),
                ('contragent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.Contragent')),
                ('unique_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bluebird.ActUN')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CountUN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CountUNGen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_when', models.DateField(blank=True, null=True)),
                ('contragent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.Contragent')),
                ('unique_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bluebird.CountUN')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='documentuniquenumbergenerator',
            name='contragent',
        ),
        migrations.RemoveField(
            model_name='documentuniquenumbergenerator',
            name='unique_number',
        ),
        migrations.DeleteModel(
            name='DocumentUniqueNumber',
        ),
        migrations.DeleteModel(
            name='DocumentUniqueNumberGenerator',
        ),
    ]