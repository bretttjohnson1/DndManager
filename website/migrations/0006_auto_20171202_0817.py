# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_user_password_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password_hash',
            field=models.CharField(max_length=512),
        ),
    ]