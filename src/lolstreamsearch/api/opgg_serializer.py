from rest_framework import serializers


class OPGGLeagueMatchRequestSerializer(serializers.Serializer):
    opgg_url = serializers.URLField(
        help_text="Full op.gg game URL",
        required=True,
    )
