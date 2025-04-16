from django.http import Http404
from elasticsearch import NotFoundError
from rest_framework import permissions, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer, ChampionKeywordSerializer, \
    OpponentChampionKeywordSerializer, RunesKeywordSerializer, ItemsKeywordSerializer, \
    TeamChampionKeywordSerializer, OpponentTeamChampionKeywordSerializer


class YtVideoListViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = YtVideoDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

class OpponentChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OpponentChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("opponent_champion")

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


class OpponentTeamChampionKeywordListViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OpponentTeamChampionKeywordSerializer

    def list(self, request, *args, **kwargs):
        return get_distinct_entries("opponent_team_champions")

def get_distinct_entries(field: str):
    search = YtVideoDocument.search()
    search.aggs.bucket("distinct_entries", "terms", field=field+".keyword", size=1000)
    response = search.execute()
    distinct_entries = [bucket.key for bucket in response.aggregations.distinct_entries.buckets]
    return Response({field: distinct_entries})
