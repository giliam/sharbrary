# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20150730_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('period', models.CharField(max_length=200)),
                ('adding_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date added to the database')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='themes',
            field=models.ManyToManyField(to='library.Theme'),
        ),
    ]
