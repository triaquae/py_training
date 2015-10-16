# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0007_auto_20150909_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(related_name='_friends_+', to='bbs.UserProfile'),
        ),
    ]
