from rest_framework.routers import DefaultRouter

from django.urls import path

from .api import views

router = DefaultRouter()
router.register(r'ytvideos', views.YtVideoListViewSet, basename='yt_video')
router.register(r'champions', views.ChampionKeywordListViewSet, basename='champions')
router.register(
    r'opponent-champions',
    views.OpponentChampionKeywordListViewSet,
    basename='opponent-champions'
)
router.register(
    r'team-champions',
    views.TeamChampionKeywordListViewSet,
    basename='team-champions'
)
router.register(
    r'opponent-team-champions',
    views.OpponentTeamChampionKeywordListViewSet,
    basename='opponent-team-champions'
)

router.register(
    r'runes',
    views.RunesKeywordListViewSet,
    basename='runes'
)

router.register(
    r'champion-items',
    views.ItemsKeywordListViewSet,
    basename='champion-items'
)


urlpatterns = router.urls + [
    path('ytvideos/activate/<str:pk>/', views.ActivateYtVideo.as_view(), name='activate-ytvideo'),
    path('ytvideos/deactivate/<str:pk>/', views.DeactivateYtVideo.as_view(), name='deactivate-ytvideo'),
]
