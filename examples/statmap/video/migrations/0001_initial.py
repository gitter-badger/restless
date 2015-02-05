# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.util
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='\u6807\u9898')),
                ('descr', models.TextField(max_length=256, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='\u6392\u5e8f\u503c')),
            ],
            options={
                'ordering': ('-order',),
                'db_table': 'video_season',
                'verbose_name': '\u5b63\u89c6\u9891\u5206\u7c7b',
                'verbose_name_plural': '\u5b63\u89c6\u9891\u5206\u7c7b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('icon', models.ImageField(upload_to=video.util.filepath, null=True, verbose_name='\u56fe\u7247', blank=True)),
                ('title', models.CharField(max_length=64, verbose_name='\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u64ad\u653e\u5730\u5740')),
                ('views', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
                ('likes', models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u91cf', editable=False)),
                ('order', models.IntegerField(default=0, verbose_name='\u6392\u5e8f\u503c')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='\u662f\u5426\u63a8\u8350')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('season', models.ForeignKey(verbose_name='\u5b63\u5206\u7c7b', to='video.Season')),
            ],
            options={
                'ordering': ('-order', '-create_time'),
                'db_table': 'video',
                'verbose_name': '\u89c6\u9891',
                'verbose_name_plural': '\u89c6\u9891',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoLiked',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('liked', models.BooleanField(default=True, verbose_name='\u662f\u5426\u70b9\u8d5e')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(verbose_name='\u89c6\u9891', to='video.Video')),
            ],
            options={
                'ordering': ('-create_time',),
                'db_table': 'video_liked',
                'verbose_name': '\u89c6\u9891\u70b9\u8d5e',
                'verbose_name_plural': '\u89c6\u9891\u70b9\u8d5e',
            },
            bases=(models.Model,),
        ),
    ]
