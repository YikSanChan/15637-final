# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 22:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0003_auto_20161124_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 24, 22, 28, 41, 832040, tzinfo=utc)),
        ),
    ]