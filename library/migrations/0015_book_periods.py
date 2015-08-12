# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_auto_20150812_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='periods',
            field=models.ManyToManyField(to='library.Period', verbose_name='periods', blank=True),
        ),
    ]
