# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 05:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0016_auto_20161124_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='locations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CSS.Location'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_menu', to='CSS.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 25, 5, 36, 21, 702032, tzinfo=utc)),
        ),
    ]
