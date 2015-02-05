from django.contrib import admin
from video.models import Season, Video, VideoLiked

admin.site.register((Season, Video, VideoLiked))
