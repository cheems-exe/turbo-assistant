# Generated by Django 3.1.2 on 2022-01-29 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 29, 16, 9, 27, 876264)),
        ),
        migrations.AlterField(
            model_name='workefficiency',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 1, 29, 16, 9, 27, 876264)),
        ),
    ]
