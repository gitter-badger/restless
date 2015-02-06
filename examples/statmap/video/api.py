# -*- coding: utf-8 -*-
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from video.models import Video, VideoLiked

__author__ = 'pobear'


class VideoLikedResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'video_id': 'video.id',
        'username': 'user.username',
        'create_time': 'create_time',
    })

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    def create(self, video_id):
        video = Video.objects.get(pk=int(video_id))
        video_liked, created = VideoLiked.objects.get_or_create(video=video, user=self.request.user)

        if not created:
            video_liked.liked = self.data['liked']
            video_liked.save()

        return video_liked

    def update(self, video_id, pk):
        video_liked = VideoLiked.objects.get(pk=pk)
        video_liked.liked = self.data['liked']
        video_liked.save()

        return video_liked

    def delete_list(self, video_id):
        return VideoLiked.objects.filter(user=self.request.user, video__id=video_id).delete()

    def list(self, video_id):
        return VideoLiked.objects.filter(video__id=int(video_id), liked=True)


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