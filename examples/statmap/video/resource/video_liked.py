# -*- coding: utf-8 -*-
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from ..models import Video, VideoLiked

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
