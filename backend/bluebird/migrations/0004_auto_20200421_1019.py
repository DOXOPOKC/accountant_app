# Generated by Django 3.0.5 on 2020-04-21 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yellowbird', '0002_auto_20200421_1019'),
        ('bluebird', '0003_auto_20200414_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_event', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_state', models.CharField(max_length=255)),
                ('departments', models.ManyToManyField(related_name='available_states', to='yellowbird.Department')),
                ('events_set', models.ManyToManyField(related_name='affected_states', to='bluebird.Event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='to_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluebird.State'),
        ),
        migrations.AddField(
            model_name='documentspackage',
            name='package_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bluebird.State'),
        ),
    ]