# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 14:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0021_auto_20161127_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='menu',
            new_name='menus',
        ),
        migrations.AlterField(
            model_name='exchange',
            name='menu',
            field=models.ForeignKey(choices=[(37, '大秋田'), (38, '小柴犬')], on_delete=django.db.models.deletion.CASCADE, related_name='exchange_menu', to='CSS.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 27, 14, 52, 2, 285751, tzinfo=utc)),
        ),
    ]