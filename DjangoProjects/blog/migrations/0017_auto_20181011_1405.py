# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20181011_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(default='blog/media/img/no_image.png', upload_to='blog/media/img/users/', verbose_name='Image'),
        ),
    ]
