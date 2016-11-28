# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 02:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0024_auto_20161127_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='image',
        ),
        migrations.AlterField(
            model_name='exchange',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_menu', to='CSS.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 28, 2, 47, 0, 196088, tzinfo=utc)),
        ),
    ]