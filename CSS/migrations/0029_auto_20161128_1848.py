# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 23:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0028_auto_20161128_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 28, 23, 48, 47, 393226, tzinfo=utc)),
        ),
    ]
