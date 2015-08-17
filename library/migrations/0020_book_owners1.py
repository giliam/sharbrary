# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0019_ownership'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='owners1',
            field=models.ManyToManyField(related_name='+', verbose_name='owner', to=settings.AUTH_USER_MODEL, through='library.Ownership', blank=True),
        ),
    ]
