# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-10 18:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0005_notice_excerpt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the account', max_length=100)),
                ('identifier', models.CharField(help_text='User identifier used for thsi account', max_length=100)),
                ('user', models.ForeignKey(help_text='User associated with this account.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
