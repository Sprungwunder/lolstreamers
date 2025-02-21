from django.http import Http404
from elasticsearch import NotFoundError
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer


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

    def list(self, request, *args, **kwargs):
        # Query for distinct champion names in the Elasticsearch index
        search = YtVideoDocument.search()
        search.aggs.bucket("distinct_champions", "terms", field="champion.keyword", size=1000)
        response = search.execute()
        distinct_champion_names = [bucket.key for bucket in
                                   response.aggregations.distinct_champions.buckets]
        return Response({"champions": distinct_champion_names})
