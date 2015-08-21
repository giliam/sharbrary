# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the library')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('status', models.CharField(default=b'OP', max_length=200, verbose_name='status of the topic', choices=[(b'OP', b'OPEN'), (b'CL', b'CLOSED'), (b'DE', b'DELETED'), (b'AR', b'ARCHIVED')])),
                ('author', models.ForeignKey(verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
