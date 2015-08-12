# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20150812_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'period',
                'verbose_name_plural': 'periods',
                'permissions': (('period_new', 'Add a period'), ('period_edit', 'Edit a period'), ('period_delete', 'Delete a period'), ('period_list', 'Show the list of periods')),
            },
        ),
        migrations.RemoveField(
            model_name='theme',
            name='period',
        ),
    ]
