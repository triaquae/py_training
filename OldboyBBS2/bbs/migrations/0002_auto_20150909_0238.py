# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(related_name='p_comment', blank=True, to='bbs.Comment', null=True),
        ),
    ]
