# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0010_auto_20151015_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('brief', models.CharField(default=b'nothing here....', max_length=254)),
                ('member_limit', models.IntegerField(default=200)),
                ('admins', models.ManyToManyField(related_name='chat_group_admins', to='bbs.UserProfile', blank=True)),
                ('founder', models.ForeignKey(to='bbs.UserProfile')),
                ('members', models.ManyToManyField(related_name='chat_group_members', to='bbs.UserProfile', blank=True)),
            ],
        ),
    ]
