# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 05:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0026_auto_20161127_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, upload_to='CSS/images/menus'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 28, 5, 26, 45, 441340, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='CSS/images/avatars'),
        ),
    ]
