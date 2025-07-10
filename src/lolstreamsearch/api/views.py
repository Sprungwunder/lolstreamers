from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from elasticsearch import NotFoundError
from rest_framework import permissions, mixins
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer, ChampionKeywordSerializer, \
    EnemyChampionKeywordSerializer, RunesKeywordSerializer, ItemsKeywordSerializer, \
    TeamChampionKeywordSerializer, EnemyTeamChampionKeywordSerializer


class YtVideoThrottle(UserRateThrottle):
    rate = '20/second'


@ensure_csrf_cookie
def get_csrf_token(request):
    """
    This view sends the CSRF token that will be used by the frontend
    """
    return JsonResponse({'csrfToken': get_token(request)})


class YtVideoListViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = YtVideoDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, YtVideoThrottle]

    def get_queryset(self):
        return YtVideoDocument.get_queryset(self.request.query_params)

    def get_object(self):
        try:
            doc = YtVideoDocument.get(id=self.kwargs.get("pk"))
            return doc
        except NotFoundError:
            raise Http404


class ChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("champion")

class EnemyChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EnemyChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("enemy_champion")

class RunesKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RunesKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("runes")

class ItemsKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ItemsKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("champion_items")

class TeamChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("team_champions")


class EnemyTeamChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EnemyTeamChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("enemy_team_champions")

def get_distinct_entries(field: str):
    search = YtVideoDocument.search()
    search = search.filter("term", **{"is_active": "true"})
    search.aggs.bucket("distinct_entries", "terms", field=field+".keyword", size=1000)
    response = search.execute()
    distinct_entries = [bucket.key for bucket in response.aggregations.distinct_entries.buckets]
    return Response({field: distinct_entries})



class ActivationApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    is_active = None

    def get_object(self):
        try:
            doc = YtVideoDocument.get(id=self.kwargs.get("pk"))
            return doc
        except NotFoundError:
            raise Http404

    def post(self, request, pk):
        ytvideo = self.get_object()
        ytvideo.set_active_and_serialize(is_active=self.is_active)
        return Response({"success": True})

class ActivateYtVideo(ActivationApiView):
    is_active = True

class DeactivateYtVideo(ActivationApiView):
    is_active = False
