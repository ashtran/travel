# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-27 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_buddy', '0002_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='companions',
            field=models.ManyToManyField(default='', related_name='plans', to='travel_buddy.User'),
        ),
    ]
