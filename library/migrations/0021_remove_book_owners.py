# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_book_owners1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='owners',
        ),
    ]
