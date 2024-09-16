from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import YtVideoListViewSet


router = DefaultRouter()
router.register(r'ytvideos', YtVideoListViewSet, basename='yt_video')

urlpatterns = router.urls
urlpatterns = urlpatterns + [
    path("", views.index, name="index"),
]
