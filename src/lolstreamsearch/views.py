from django.http import Http404
from django.shortcuts import render
from elasticsearch import NotFoundError
from rest_framework import permissions, viewsets

from lolstreamsearch.models import YtStream
from lolstreamsearch.yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer


def index(request):
    latest_stream_list = YtStream.objects.order_by("-streamer_name")[:5]
    context = {"latest_stream_list": latest_stream_list, }
    return render(request, "lolstreamsearch/index.html", context)


class YtVideoListViewSet(viewsets.ModelViewSet):
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
