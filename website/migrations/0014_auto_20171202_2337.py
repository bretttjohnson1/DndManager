# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 23:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20171202_2327'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='armor',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='weapon',
            unique_together=set([]),
        ),
    ]