# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0025_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='value',
            field=models.PositiveIntegerField(choices=[(0, 'DO NOT READ IT'), (1, 'This is bad.'), (2, 'Humpf'), (3, 'Not so bad'), (4, 'Liked it!'), (5, 'READ IT')]),
        ),
    ]
