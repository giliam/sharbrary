# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20150804_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='editor',
            field=models.ForeignKey(default='', blank=True, to='library.Editor'),
            preserve_default=False,
        ),
    ]
