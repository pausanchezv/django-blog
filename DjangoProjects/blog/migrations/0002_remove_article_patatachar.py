# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 06:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='patatachar',
        ),
    ]