# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0005_auto_20150810_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lending',
            options={'default_permissions': [], 'verbose_name': 'lending', 'verbose_name_plural': 'lendings', 'permissions': (('lending_new', 'Add a lending'), ('lending_edit', 'Edit a lending'), ('lending_delete', 'Delete a lending'), ('lending_list', 'Show the list of lendings'))},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'default_permissions': [], 'verbose_name': 'profile', 'verbose_name_plural': 'profiles', 'permissions': (('profile_new', 'Add a profile'), ('profile_edit', 'Edit a profile'), ('profile_delete', 'Delete a profile'), ('profile_list', 'Show the list of profiles'), ('profile_show', 'Show a profile'))},
        ),
        migrations.AlterField(
            model_name='profile',
            name='informations',
            field=models.TextField(verbose_name='informations', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, verbose_name='phone number', validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '0123456789'. Up to 15 digits allowed.")]),
        ),
    ]
