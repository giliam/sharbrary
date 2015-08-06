# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0008_auto_20150804_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False)),
                ('beginning_date', models.DateTimeField(null=True, verbose_name=b'beginning date of the lending', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name=b'end date of the lending', blank=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date added to the database')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name=b'date updated to the database')),
                ('book', models.ForeignKey(to='library.Book')),
                ('borrower', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
