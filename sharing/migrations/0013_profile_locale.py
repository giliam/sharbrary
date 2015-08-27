# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0012_auto_20150824_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='locale',
            field=models.CharField(default=b'fr', max_length=6, verbose_name='locale language', choices=[(b'fr', b'Fran\xc3\xa7ais'), (b'en', b'English')]),
        ),
    ]
