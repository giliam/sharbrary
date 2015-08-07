# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0002_auto_20150806_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lending',
            name='book',
            field=models.ForeignKey(verbose_name='book', to='library.Book'),
        ),
        migrations.AlterField(
            model_name='lending',
            name='borrower',
            field=models.ForeignKey(verbose_name='borrower', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lending',
            name='status',
            field=models.BooleanField(default=False, help_text='is it lent now ?', verbose_name='status'),
        ),
    ]
