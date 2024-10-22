from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import views


router = DefaultRouter()
router.register(r'ytvideos', views.YtVideoListViewSet, basename='yt_video')

urlpatterns = router.urls
