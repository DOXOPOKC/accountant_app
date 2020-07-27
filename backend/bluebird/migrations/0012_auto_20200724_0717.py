# Generated by Django 3.0.7 on 2020-07-24 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bluebird', '0011_auto_20200710_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='Путь')),
            ],
        ),
        migrations.CreateModel(
            name='ContragentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
        ),
        migrations.RenameField(
            model_name='adress',
            old_name='house_number',
            new_name='block',
        ),
        migrations.AddField(
            model_name='adress',
            name='state',
            field=models.CharField(default='-', max_length=255, verbose_name='Область'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contragent',
            name='klass',
            field=models.IntegerField(choices=[(0, 'Пусто'), (1, 'Юридическое лицо без договора'), (2, 'Юридическое лицо с договором'), (3, 'ИЖС без договора'), (4, 'ИЖС с договором'), (5, 'Физическое лицо')], default=0),
        ),
        migrations.AddField(
            model_name='documentspackage',
            name='act',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.ActExam'),
        ),
    ]
