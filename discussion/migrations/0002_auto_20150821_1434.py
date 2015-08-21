# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(verbose_name='message')),
                ('added_date', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('author', models.ForeignKey(verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='discussion',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date added'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date updated'),
        ),
        migrations.AddField(
            model_name='message',
            name='discussion',
            field=models.ManyToManyField(related_name='messages', to='discussion.Discussion'),
        ),
    ]
