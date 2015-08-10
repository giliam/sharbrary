# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20150807_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'default_permissions': [], 'verbose_name': 'author', 'verbose_name_plural': 'authors', 'permissions': (('author_new', 'Add an author'), ('author_edit', 'Edit an author'), ('author_delete', 'Delete an author'), ('author_list', 'Show the list of authors'))},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'default_permissions': [], 'verbose_name': 'book', 'verbose_name_plural': 'books', 'permissions': (('book_new', 'Add a book'), ('book_edit', 'Edit a book'), ('book_delete', 'Delete a book'), ('book_list', 'Show the list of books'))},
        ),
        migrations.AlterModelOptions(
            name='editor',
            options={'default_permissions': [], 'verbose_name': 'editor', 'verbose_name_plural': 'editors', 'permissions': (('editor_new', 'Add an editor'), ('editor_edit', 'Edit an editor'), ('editor_delete', 'Delete an editor'), ('editor_list', 'Show the list of editors'))},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'default_permissions': [], 'verbose_name': 'theme', 'verbose_name_plural': 'themes', 'permissions': (('theme_new', 'Add a theme'), ('theme_edit', 'Edit a theme'), ('theme_delete', 'Delete a theme'), ('theme_list', 'Show the list of themes'))},
        ),
    ]
