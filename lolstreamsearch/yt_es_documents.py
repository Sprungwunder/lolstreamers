"""
Youtube Elasticsearch Documents Model
"""
from typing import List

from elasticsearch_dsl import Text, Date, Keyword, Document
from rest_framework import serializers


class YtVideoDocument(Document):
    title = Text()
    description = Text()
    video_url = Text()
    published_at = Date()
    champion = Keyword()
    opponent_champion = Keyword()
    lane = Keyword()
    runes = Text(multi=True)
    items = Text(multi=True)
    lol_version = Keyword()

    class Index:
        name = 'lolstreamsearch_yt_videos'
        settings = {
            'number_of_shards': 1,
            'auto_expand_replicas': '0-1'
        }

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'published_at': self.published_at,
            'champion': self.champion,
            'opponent_champion': self.opponent_champion,
            'lane': self.lane,
            'runes': self.runes,
            'items': self.items,
            'lol_version': self.lol_version,
        }

    @staticmethod
    def get_queryset():
        videos = YtVideoDocument.search()
        video_list = [hit.serialize() for hit in videos]
        return video_list


class YtVideoDocumentSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    video_url = serializers.CharField()
    published_at = serializers.DateTimeField()
    champion = serializers.CharField()
    opponent_champion = serializers.CharField()
    lane = serializers.CharField()
    runes = serializers.ListSerializer(child=serializers.CharField())
    items = serializers.ListSerializer(child=serializers.CharField())
    lol_version = serializers.CharField()

    def validate(self, data):
        return data

    def create(self, validated_data):
        ytvideo = YtVideoDocument(**validated_data)
        if ytvideo.save() == "created":
            return ytvideo
