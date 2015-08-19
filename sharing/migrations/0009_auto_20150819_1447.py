# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from utils.groups.create_groups import add_groups

class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0008_auto_20150817_1637'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]
