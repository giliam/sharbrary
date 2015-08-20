# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0008_auto_20150817_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(upload_to=b'profile_picture/', null=True, verbose_name='picture', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, verbose_name='phone number', validators=[django.core.validators.RegexValidator(regex=b'^(\\d{2}( |-)?){5}$', message="Phone number must be entered in the format: '0123456789'. Up to 10 digits allowed.")]),
        ),
    ]
