# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20181009_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Client'),
        ),
    ]
