# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_auto_20150813_1126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'default_permissions': [], 'verbose_name': 'book', 'verbose_name_plural': 'books', 'permissions': (('book_new', 'Add a book'), ('book_detail', 'Show a book page'), ('book_edit', 'Edit a book'), ('book_delete', 'Delete a book'), ('book_remove_from_library', 'Remove a book from your library'), ('book_remove_from_all_libraries', 'Remove a book from all libraries'), ('book_list', 'Show the list of books'))},
        ),
    ]
