# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 06:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0018_auto_20161125_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CSS.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 25, 6, 14, 12, 654642, tzinfo=utc)),
        ),
    ]
