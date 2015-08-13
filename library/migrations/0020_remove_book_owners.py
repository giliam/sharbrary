# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_auto_20150813_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='owners',
        ),
    ]
