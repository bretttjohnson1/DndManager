# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20171202_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_salt',
            field=models.CharField(default='', max_length=40),
        ),
    ]
