# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0009_usergroup_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='online',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
