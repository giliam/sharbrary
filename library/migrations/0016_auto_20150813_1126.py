# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0015_book_periods'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'default_permissions': [], 'verbose_name': 'author', 'verbose_name_plural': 'authors', 'permissions': (('author_new', 'Add an author'), ('author_detail', 'Show an author details'), ('author_edit', 'Edit an author'), ('author_delete', 'Delete an author'), ('author_list', 'Show the list of authors'))},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'default_permissions': [], 'verbose_name': 'book', 'verbose_name_plural': 'books', 'permissions': (('book_new', 'Add a book'), ('book_detail', 'Show a book page'), ('book_edit', 'Edit a book'), ('book_delete', 'Delete a book'), ('book_list', 'Show the list of books'))},
        ),
        migrations.RemoveField(
            model_name='book',
            name='owner',
        ),
        migrations.AddField(
            model_name='book',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='owner', blank=True),
        ),
    ]
