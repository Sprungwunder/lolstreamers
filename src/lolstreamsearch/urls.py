from rest_framework.routers import DefaultRouter

from django.urls import path

from .api import views

router = DefaultRouter()
router.register(r'ytvideos', views.YtVideoListViewSet, basename='yt_video')
router.register(r'champions', views.ChampionKeywordListViewSet, basename='champions')
router.register(
    r'enemy-champions',
    views.EnemyChampionKeywordListViewSet,
    basename='enemy-champions'
)
router.register(
    r'team-champions',
    views.TeamChampionKeywordListViewSet,
    basename='team-champions'
)
router.register(
    r'enemy-team-champions',
    views.EnemyTeamChampionKeywordListViewSet,
    basename='enemy-team-champions'
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

router.register(
    'streamers',
    views.StreamerKeywordListViewSet,
    basename='streamers'
)


urlpatterns = router.urls + [
    path('ytvideos/activate/<str:pk>/', views.ActivateYtVideo.as_view(), name='activate-ytvideo'),
    path('ytvideos/deactivate/<str:pk>/', views.DeactivateYtVideo.as_view(), name='deactivate-ytvideo'),
    path('ytvideos/check-duplicate/<str:ytid>/', views.CheckDuplicateYtVideo.as_view(), name='check-duplicate-ytvideo'),
    path('ytvideos/league-match/opgg/', views.LeagueMatchAPIView.as_view(), name='league-opgg-match'),
    path('ytvideos/league-match/yt/', views.LeagueMatchFromYTVideoAPIView.as_view(), name='league-yt-match')
]
