# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('birthdate', models.DateTimeField(verbose_name=b'birthdate')),
                ('death_date', models.DateTimeField(verbose_name=b'date of death')),
                ('adding_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date added to the database')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('publishing_date', models.DateTimeField(verbose_name=b'date published')),
                ('adding_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date added to the library')),
                ('author', models.ForeignKey(to='library.Author')),
            ],
        ),
        migrations.DeleteModel(
            name='Livre',
        ),
    ]
