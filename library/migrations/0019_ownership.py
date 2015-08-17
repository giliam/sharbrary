# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0018_auto_20150813_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copies', models.PositiveIntegerField(default=1, verbose_name='number of copies', blank=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added to the library')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('comments', models.TextField(default=b'', verbose_name='comments', blank=True)),
                ('cover', models.ImageField(upload_to=b'cover/', null=True, verbose_name='cover', blank=True)),
                ('book', models.ForeignKey(verbose_name='book', to='library.Book')),
                ('editor', models.ForeignKey(verbose_name='editor', blank=True, to='library.Editor', null=True)),
                ('owner', models.ForeignKey(verbose_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'ownership',
                'verbose_name_plural': 'ownerships',
                'permissions': (('ownership_new', 'Have a book'), ('ownership_edit', 'Edit a ownership'), ('ownership_delete', 'Delete a ownership')),
            },
        ),
    ]
