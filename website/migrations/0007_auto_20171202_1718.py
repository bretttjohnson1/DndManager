# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20171202_0817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='user_id',
            new_name='user_name',
        ),
    ]
