# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from util import filepath
from django.contrib.auth.models import User

__author__ = 'pobear'


class Season(models.Model):
    name = models.CharField(_(u'标题'), max_length=16)
    descr = models.TextField(_(u'描述'), max_length=256, null=True, blank=True)
    order = models.IntegerField(_(u'排序值'), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'video_season'
        verbose_name = '季视频分类'
        verbose_name_plural = verbose_name
        ordering = ('-order',)


class Video(models.Model):
    season = models.ForeignKey(Season, verbose_name=_(u'季分类'))
    icon = models.ImageField(_(u'图片'), upload_to=filepath, blank=True, null=True)
    title = models.CharField(_(u'标题'), max_length=64)
    url = models.URLField(_(u'播放地址'))
    views = models.IntegerField(_(u'浏览量'), default=0)
    likes = models.IntegerField(_(u'点赞量'), default=0, editable=False)
    order = models.IntegerField(_(u'排序值'), default=0)
    is_recommend = models.BooleanField(_(u'是否推荐'), default=False)

    create_time = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    update_time = models.DateTimeField(_(u'更新时间'), auto_now=True)

    def descr(self):
        return u'%s-%s' % (self.season, self.title)

    def icon_url(self):
        return self.icon and self.icon.url or None

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ('-order', '-create_time',)


class VideoLiked(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'用户'))
    video = models.ForeignKey(Video, verbose_name=_(u'视频'))
    liked = models.BooleanField(_(u'是否点赞'), default=True)

    create_time = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    update_time = models.DateTimeField(_(u'更新时间'), auto_now=True)

    def __unicode__(self):
        return '%s:%s' % (self.user.username, self.video.title)

    class Meta:
        db_table = 'video_liked'
        verbose_name = '视频点赞'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)