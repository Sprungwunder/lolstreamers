from django.urls import path

from . import views
from .views import YtVideoView

urlpatterns = [
    path("", views.index, name="index"),
    path("api/yt-video/", YtVideoView.as_view(), name="yt_video"),
]
