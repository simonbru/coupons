# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 11:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0006_auto_20170717_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ('name',), 'verbose_name': 'restaurant', 'verbose_name_plural': 'restaurants'},
        ),
    ]
