# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharing', '0003_auto_20150807_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('informations', models.TextField(blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '0123456789'. Up to 15 digits allowed.")])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
