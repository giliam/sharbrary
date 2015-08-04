# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20150804_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birthdate',
            field=models.DateTimeField(verbose_name=b'birthdate', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='death_date',
            field=models.DateTimeField(verbose_name=b'date of death', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(to='library.Author', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publishing_date',
            field=models.DateTimeField(verbose_name=b'date published', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='themes',
            field=models.ManyToManyField(to='library.Theme', blank=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='period',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
