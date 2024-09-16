from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from lolstreamsearch.elasticsearch_api import YtVideoElasticAPI
from lolstreamsearch.models import YtStream
from lolstreamsearch.yt_es_documents import YtVideoDocument


def index(request):
    latest_stream_list = YtStream.objects.order_by("-streamer_name")[:5]
    context = {"latest_stream_list": latest_stream_list, }
    return render(request, "lolstreamsearch/index.html", context)


class YtVideoView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        videos = YtVideoElasticAPI.get_all_videos(request.query_params.get('q', ''))
        video_list = [hit.serialize() for hit in videos]
        return Response(video_list)

    def post(self, request):
        return Response({"message": "Hello Admin"})
