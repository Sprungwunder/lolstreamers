from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lolstreamsearch.models import YtStream


def index(request):
    latest_stream_list = YtStream.objects.order_by("-streamer_name")[:5]
    context = {"latest_stream_list": latest_stream_list, }
    return render(request, "lolstreamsearch/index.html", context)


class YtVideoView(APIView):
    @permission_classes([AllowAny])
    def get(self, request):
        return Response({"message": "Hello User"})

    @permission_classes([IsAdminUser])
    def post(self, request):
        return Response({"message": "Hello Admin"})
