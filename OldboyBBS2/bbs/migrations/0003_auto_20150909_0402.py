# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0002_auto_20150909_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs',
            name='breif',
            field=models.TextField(default=b'none.....', max_length=512),
        ),
        migrations.AddField(
            model_name='bbs',
            name='head_img',
            field=models.ImageField(default=None, upload_to=b''),
        ),
    ]
