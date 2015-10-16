# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0003_auto_20150909_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs',
            name='head_img',
            field=models.ImageField(upload_to=b''),
        ),
    ]
