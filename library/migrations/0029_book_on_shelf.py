# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0028_page_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='on_shelf',
            field=models.BooleanField(default=True),
        ),
    ]
