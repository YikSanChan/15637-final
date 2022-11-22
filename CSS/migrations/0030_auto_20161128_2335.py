# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 04:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('CSS', '0029_auto_20161128_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='menu',
            field=models.ForeignKey(choices=[(3, '香香的牛排'), (4, '辣辣的鱼')], on_delete=django.db.models.deletion.CASCADE, related_name='exchange_menu', to='CSS.Menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 29, 4, 35, 40, 141670, tzinfo=utc)),
        ),
    ]