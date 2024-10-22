"""
Youtube Elasticsearch Documents Model
"""
from elasticsearch_dsl import Text, Date, Keyword, Document
from rest_framework import serializers

from google_api import get_yt_video_information


class YtVideoDocument(Document):
    id = Keyword()
    title = Text()
    description = Text()
    video_url = Text()
    published_at = Date()
    champion = Keyword()
    opponent_champion = Keyword()
    team_champion = Keyword()
    opponent_team_champion = Keyword(multi=True)
    lane = Keyword()
    runes = Keyword(multi=True)
    champion_items = Keyword(multi=True)
    lol_version = Keyword()
    streamer = Keyword()

    class Index:
        name = 'lolstreamsearch_yt_videos'
        settings = {
            'number_of_shards': 1,
            'auto_expand_replicas': '0-1'
        }

    def serialize(self):
        return {
            'id': self.meta.id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'published_at': self.published_at,
            'champion': self.champion,
            'opponent_champion': self.opponent_champion,
            'team_champions': self.team_champions,
            'opponent_team_champions': self.opponent_team_champions,
            'lane': self.lane,
            'runes': self.runes,
            'champion_items': self.champion_items,
            'lol_version': self.lol_version,
            'streamer': self.streamer
        }

    @staticmethod
    def get_queryset():
        videos = YtVideoDocument.search()
        video_list = [hit.serialize() for hit in videos]
        return video_list


class YtVideoDocumentSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    video_url = serializers.CharField()
    published_at = serializers.DateTimeField(required=False)
    champion = serializers.CharField()
    opponent_champion = serializers.CharField()
    team_champions = serializers.ListField(child=serializers.CharField())
    opponent_team_champions = serializers.ListSerializer(child=serializers.CharField())
    lane = serializers.CharField()
    runes = serializers.ListSerializer(child=serializers.CharField())
    champion_items = serializers.ListSerializer(child=serializers.CharField())
    lol_version = serializers.CharField()
    streamer = serializers.CharField(required=False)
    views = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)

    def get_yt_id(self, instance):
        return instance["video_url"].split("v=")[1]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, YtVideoDocument):
            representation['id'] = instance.meta.id

        yt_info = get_yt_video_information(self.get_yt_id(instance))
        representation['views'] = yt_info.views
        representation['likes'] = yt_info.likes
        return representation

    def create(self, validated_data):
        if 'id' in validated_data:
            del validated_data['id']
        yt_video_info = get_yt_video_information(self.get_yt_id(validated_data))
        validated_data['title'] = yt_video_info.title
        validated_data['description'] = yt_video_info.description
        validated_data['published_at'] = yt_video_info.published_at
        validated_data['streamer'] = yt_video_info.channel
        ytvideo = YtVideoDocument(**validated_data)
        result = ytvideo.save(return_doc_meta=True)
        meta_id = result.body.get("_id")
        ytvideo.meta.id = meta_id
        ytvideo.id = meta_id
        return ytvideo
