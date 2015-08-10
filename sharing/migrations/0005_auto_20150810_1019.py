# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0004_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lending',
            options={'verbose_name': 'lending', 'verbose_name_plural': 'lendings'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
    ]
