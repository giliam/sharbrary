# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_auto_20150820_1615'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sharing', '0010_auto_20150821_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fulfilled', models.BooleanField(default=False)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('book_copy', models.ForeignKey(verbose_name='book copy', to='library.Ownership')),
                ('borrower', models.ForeignKey(verbose_name='borrower', blank=True, to=settings.AUTH_USER_MODEL)),
                ('lending', models.ForeignKey(verbose_name='lending', blank=True, to='sharing.Lending')),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'queue',
                'verbose_name_plural': 'queues',
                'permissions': (('queue_new', 'Add a queue'), ('queue_edit', 'Edit a queue'), ('queue_delete', 'Delete a queue'), ('queue_list', 'Show the list of queues')),
            },
        ),
    ]
