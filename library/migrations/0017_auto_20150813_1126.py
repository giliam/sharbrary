# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_auto_20150813_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='owner', blank=True),
        ),
    ]
