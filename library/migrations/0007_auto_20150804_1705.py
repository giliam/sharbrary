# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_book_editor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, to='library.Author', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='editor',
            field=models.ForeignKey(blank=True, to='library.Editor', null=True),
        ),
    ]
