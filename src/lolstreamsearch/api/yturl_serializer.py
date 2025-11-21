from rest_framework import serializers


class YtURLSerializer(serializers.Serializer):
    yt_url = serializers.URLField(
        help_text="Youtube commentary URL",
        required=True,
    )
