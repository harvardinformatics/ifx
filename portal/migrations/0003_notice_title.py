# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-23 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20180123_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='title',
            field=models.CharField(default='title', help_text='Title for the notice', max_length=100),
            preserve_default=False,
        ),
    ]