# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 06:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0017_auto_20161125_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='locations',
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 25, 6, 12, 32, 66328, tzinfo=utc)),
        ),
    ]
