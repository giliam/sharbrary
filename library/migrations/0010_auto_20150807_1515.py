# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_book_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'book', 'verbose_name_plural': 'books'},
        ),
        migrations.AlterModelOptions(
            name='editor',
            options={'verbose_name': 'editor', 'verbose_name_plural': 'editors'},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'verbose_name': 'theme', 'verbose_name_plural': 'themes'},
        ),
        migrations.AlterField(
            model_name='author',
            name='firstname',
            field=models.CharField(max_length=200, verbose_name='firstname'),
        ),
        migrations.AlterField(
            model_name='author',
            name='lastname',
            field=models.CharField(max_length=200, verbose_name='lastname'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(verbose_name='author', blank=True, to='library.Author', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='editor',
            field=models.ForeignKey(verbose_name='editor', blank=True, to='library.Editor', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(default=b'', verbose_name='summary', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='themes',
            field=models.ManyToManyField(to='library.Theme', verbose_name='themes', blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='period',
            field=models.CharField(max_length=200, verbose_name='period', blank=True),
        ),
    ]
