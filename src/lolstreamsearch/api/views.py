from django.http import Http404
from elasticsearch import NotFoundError
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from .yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer


class YtVideoListViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = YtVideoDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return YtVideoDocument.get_queryset()

    def get_object(self):
        try:
            doc = YtVideoDocument.get(id=self.kwargs.get("pk"))
            return doc
        except NotFoundError:
            raise Http404
