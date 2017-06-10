# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-10 20:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Wager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='Winner',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bet',
            name='Due_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 11, 20, 22, 5, 333277, tzinfo=utc)),
        ),
    ]