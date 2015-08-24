# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0011_queue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='lending',
            field=models.ForeignKey(verbose_name='lending', blank=True, to='sharing.Lending', null=True),
        ),
    ]
