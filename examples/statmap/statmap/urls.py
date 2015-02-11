# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from video.resource.video import VideoResource
from video.resource.video_liked import VideoLikedResource

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^videos/', include(VideoResource.urls())),
                       # 符合Restful API的url设计
                       url(r'^videos/(?P<video_id>\d+)/likes/', include(VideoLikedResource.urls())),
                       )

if settings.DEBUG:
    urlpatterns = urlpatterns \
                  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)