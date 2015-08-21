# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0002_auto_20150821_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discussion',
            options={'ordering': ['-updated_date', 'title'], 'default_permissions': [], 'verbose_name': 'discussion', 'verbose_name_plural': 'discussions', 'permissions': (('discussion_new', 'Add an discussion'), ('discussion_detail', 'Show a discussion details'), ('discussion_edit', 'Edit a discussion'), ('discussion_delete', 'Delete a discussion'), ('discussion_list', 'Show the list of discussions'))},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-added_date'], 'default_permissions': [], 'verbose_name': 'message', 'verbose_name_plural': 'messages', 'permissions': (('message_new', 'Add an message'), ('message_detail', 'Show a message details'), ('message_edit', 'Edit a message'), ('message_delete', 'Delete a message'), ('message_list', 'Show the list of messages'))},
        ),
    ]
