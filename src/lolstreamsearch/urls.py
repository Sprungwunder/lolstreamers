from rest_framework.routers import DefaultRouter

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

urlpatterns = router.urls
