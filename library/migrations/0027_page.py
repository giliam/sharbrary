# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0026_auto_20150902_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name of the page')),
                ('content', models.TextField(default=b'', verbose_name='content of the page')),
            ],
            options={
                'ordering': ['name'],
                'default_permissions': [],
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'permissions': (('page_new', 'Create a page'), ('page_edit', 'Edit a page'), ('page_moderate', 'Moderate a page'), ('page_delete', 'Delete a page')),
            },
        ),
    ]
