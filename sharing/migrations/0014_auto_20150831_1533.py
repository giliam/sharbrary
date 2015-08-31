# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0013_profile_locale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lending',
            options={'default_permissions': [], 'verbose_name': 'lending', 'verbose_name_plural': 'lendings', 'permissions': (('lending_new', 'Add a lending'), ('lending_edit', 'Edit a lending'), ('lending_moderate', 'Moderate a lending'), ('lending_delete', 'Delete a lending'), ('lending_list', 'Show the list of lendings'))},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'default_permissions': [], 'verbose_name': 'profile', 'verbose_name_plural': 'profiles', 'permissions': (('profile_new', 'Add a profile'), ('profile_edit', 'Edit a profile'), ('profile_moderate', 'Moderate a profile'), ('profile_delete', 'Delete a profile'), ('profile_list', 'Show the list of profiles'), ('profile_show', 'Show a profile'))},
        ),
        migrations.AlterModelOptions(
            name='queue',
            options={'default_permissions': [], 'verbose_name': 'queue', 'verbose_name_plural': 'queues', 'permissions': (('queue_new', 'Add a queue'), ('queue_edit', 'Edit a queue'), ('queue_moderate', 'Moderate a queue'), ('queue_delete', 'Delete a queue'), ('queue_list', 'Show the list of queues'))},
        ),
    ]
