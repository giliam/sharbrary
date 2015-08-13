# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_remove_book_owners'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='owners1',
            new_name='owners',
        ),
    ]
