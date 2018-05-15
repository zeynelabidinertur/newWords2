# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-15 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20180515_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='albums',
        ),
        migrations.AddField(
            model_name='myuser',
            name='bookshelf',
            field=models.ManyToManyField(blank=True, null=True, to='music.Bookshelf'),
        ),
    ]