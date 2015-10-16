# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=254)),
                ('content', models.TextField(max_length=100000)),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=1024)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bbs', models.ForeignKey(to='bbs.BBS')),
                ('parent_comment', models.ForeignKey(related_name='p_comment', blank=True, to='bbs.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Thumb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=32, choices=[(b'thumb_up', b'Thumb Up'), (b'view_count', b'View Count')])),
                ('bbs', models.ForeignKey(to='bbs.BBS')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_groups', models.ManyToManyField(to='bbs.UserGroup')),
            ],
        ),
        migrations.AddField(
            model_name='thumb',
            name='user',
            field=models.ForeignKey(to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='bbs',
            name='author',
            field=models.ForeignKey(to='bbs.UserProfile'),
        ),
        migrations.AddField(
            model_name='bbs',
            name='category',
            field=models.ForeignKey(to='bbs.Category'),
        ),
    ]
