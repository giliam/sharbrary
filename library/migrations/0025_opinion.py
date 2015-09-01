# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0024_auto_20150831_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated to the database')),
                ('value', models.PositiveIntegerField(choices=[(0, 'DO NOT READ IT'), (1, 'Humpf'), (2, 'Why not?'), (3, 'Not so bad'), (4, 'Liked it!'), (5, 'READ IT')])),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(verbose_name='book', to='library.Book')),
            ],
            options={
                'ordering': ['book__title', 'author__username'],
                'default_permissions': [],
                'verbose_name': 'opinion',
                'verbose_name_plural': 'opinions',
                'permissions': (('opinion_new', 'Have an opinion'), ('opinion_edit', 'Edit an opinion'), ('opinion_moderate', 'Moderate an opinion'), ('opinion_delete', 'Delete an opinion')),
            },
        ),
    ]
