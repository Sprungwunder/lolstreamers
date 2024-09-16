from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from lolstreamsearch.elasticsearch_api import YtVideoElasticAPI
from lolstreamsearch.models import YtStream
from lolstreamsearch.yt_es_documents import YtVideoDocument, YtVideoDocumentSerializer


def index(request):
    latest_stream_list = YtStream.objects.order_by("-streamer_name")[:5]
    context = {"latest_stream_list": latest_stream_list, }
    return render(request, "lolstreamsearch/index.html", context)


class YtVideoListViewSet(viewsets.ModelViewSet):
    queryset = YtVideoDocument.get_queryset()
    serializer_class = YtVideoDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
