# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0006_auto_20150810_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lending',
            name='status',
        ),
    ]
