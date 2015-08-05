# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20150804_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birthdate',
            field=models.DateTimeField(null=True, verbose_name=b'birthdate', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_date',
            field=models.DateTimeField(null=True, verbose_name=b'date of death', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publishing_date',
            field=models.DateTimeField(null=True, verbose_name=b'date published', blank=True),
        ),
    ]
