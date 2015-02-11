# -*- coding: utf-8 -*-
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from ..models import Video
from .video_liked import VideoLikedResource

__author__ = 'pobear'


class VideoResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'icon': 'icon_url',
        'title': 'descr',
        'url': 'url',
        'season': 'season.name',
        'views': 'views',
        'likes': 'likes',
        'liked': 'liked?',
        'update_time': 'update_time',
        # users 成为下一个preparer对应的数据节点
        'users': VideoLikedResource.preparer,
        'create_date': 'create_date?',
        'time': 'time?',
    })

    def is_authenticated(self):
        if not self.request_method() == 'GET':
            return self.request.user.is_authenticated()

        return True

    def list(self):
        return Video.objects.select_related('season').all()

    def detail(self, pk):
        video = Video.objects.select_related('season').get(pk=pk)

        video.users = video.videoliked_set.filter(liked=True)[:5]
        video.liked = len(video.users) > 0
        video.create_date = video.update_time.date()
        video.time = video.update_time.time()
        print 'video.users=', video.users

        return video