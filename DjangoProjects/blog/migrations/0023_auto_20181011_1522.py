# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20181011_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(default='blog/profile/no_image.png', upload_to='profile', verbose_name='Image'),
        ),
    ]
