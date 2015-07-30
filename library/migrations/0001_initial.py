# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=200)),
                ('annee_parution', models.DateTimeField(verbose_name=b'date published')),
                ('date_ajout', models.DateTimeField(verbose_name=b'date added to the library')),
            ],
        ),
    ]
