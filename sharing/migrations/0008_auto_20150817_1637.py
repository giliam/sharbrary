# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0007_remove_lending_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lending',
            name='beginning_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='beginning date of the lending', blank=True),
        ),
    ]
