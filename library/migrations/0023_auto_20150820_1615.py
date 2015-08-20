# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_auto_20150817_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['lastname', 'firstname'], 'default_permissions': [], 'verbose_name': 'author', 'verbose_name_plural': 'authors', 'permissions': (('author_new', 'Add an author'), ('author_detail', 'Show an author details'), ('author_edit', 'Edit an author'), ('author_delete', 'Delete an author'), ('author_list', 'Show the list of authors'))},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title'], 'default_permissions': [], 'verbose_name': 'book', 'verbose_name_plural': 'books', 'permissions': (('book_new', 'Add a book'), ('book_detail', 'Show a book page'), ('book_edit', 'Edit a book'), ('book_delete', 'Delete a book'), ('book_remove_from_library', 'Remove a book from your library'), ('book_remove_from_all_libraries', 'Remove a book from all libraries'), ('book_list', 'Show the list of books'))},
        ),
        migrations.AlterModelOptions(
            name='editor',
            options={'ordering': ['name'], 'default_permissions': [], 'verbose_name': 'editor', 'verbose_name_plural': 'editors', 'permissions': (('editor_new', 'Add an editor'), ('editor_edit', 'Edit an editor'), ('editor_delete', 'Delete an editor'), ('editor_list', 'Show the list of editors'))},
        ),
        migrations.AlterModelOptions(
            name='ownership',
            options={'ordering': ['book__title', 'owner__username'], 'default_permissions': [], 'verbose_name': 'ownership', 'verbose_name_plural': 'ownerships', 'permissions': (('ownership_new', 'Have a book'), ('ownership_edit', 'Edit a ownership'), ('ownership_delete', 'Delete a ownership'))},
        ),
        migrations.AlterModelOptions(
            name='period',
            options={'ordering': ['name'], 'default_permissions': [], 'verbose_name': 'period', 'verbose_name_plural': 'periods', 'permissions': (('period_new', 'Add a period'), ('period_edit', 'Edit a period'), ('period_delete', 'Delete a period'), ('period_list', 'Show the list of periods'))},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'ordering': ['name'], 'default_permissions': [], 'verbose_name': 'theme', 'verbose_name_plural': 'themes', 'permissions': (('theme_new', 'Add a theme'), ('theme_edit', 'Edit a theme'), ('theme_delete', 'Delete a theme'), ('theme_list', 'Show the list of themes'))},
        ),
    ]
