# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0008_userprofile_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='QQGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('member_limit', models.IntegerField(default=200)),
                ('admins', models.ManyToManyField(related_name='group_admins', to='bbs.UserProfile', blank=True)),
                ('founder', models.ForeignKey(to='bbs.UserProfile')),
                ('members', models.ManyToManyField(related_name='group_members', to='bbs.UserProfile', blank=True)),
            ],
        ),
    ]
