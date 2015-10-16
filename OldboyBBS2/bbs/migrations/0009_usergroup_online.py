# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0008_userprofile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
