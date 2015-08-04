# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20150804_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='adding_date',
            new_name='added_date',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='adding_date',
            new_name='added_date',
        ),
        migrations.RenameField(
            model_name='theme',
            old_name='adding_date',
            new_name='added_date',
        ),
        migrations.AddField(
            model_name='author',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 11, 16, 21, 737000, tzinfo=utc), verbose_name=b'date updated to the database', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 11, 16, 25, 489000, tzinfo=utc), verbose_name=b'date updated to the database', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editor',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 11, 16, 27, 874000, tzinfo=utc), verbose_name=b'date added to the database', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 11, 16, 29, 946000, tzinfo=utc), verbose_name=b'date updated to the database', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 11, 16, 32, 962000, tzinfo=utc), verbose_name=b'date updated to the database', auto_now=True),
            preserve_default=False,
        ),
    ]
