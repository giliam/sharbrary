# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_auto_20150821_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='discussion',
        ),
        migrations.AddField(
            model_name='message',
            name='discussion',
            field=models.ForeignKey(related_name='messages', default='', to='discussion.Discussion'),
            preserve_default=False,
        ),
    ]
