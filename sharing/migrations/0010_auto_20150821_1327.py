# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_auto_20150820_1615'),
        ('sharing', '0009_auto_20150820_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lending',
            name='book',
        ),
        migrations.AddField(
            model_name='lending',
            name='book_copy',
            field=models.ForeignKey(default='', verbose_name='book copy', to='library.Ownership'),
            preserve_default=False,
        ),
    ]
