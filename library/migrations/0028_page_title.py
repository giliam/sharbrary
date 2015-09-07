# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0027_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='title of the page'),
            preserve_default=False,
        ),
    ]
