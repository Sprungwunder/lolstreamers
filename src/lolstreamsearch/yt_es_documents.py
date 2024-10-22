"""
Youtube Elasticsearch Documents Model
"""
from elasticsearch_dsl import Text, Date, Keyword, Document
from rest_framework import serializers


class YtVideoDocument(Document):
    id = Keyword()
    title = Text()
    description = Text()
    video_url = Text()
    published_at = Date()
    champion = Keyword()
    opponent_champion = Keyword()
    lane = Keyword()
    runes = Text(multi=True)
    champion_items = Text(multi=True)
    lol_version = Keyword()

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
            'lane': self.lane,
            'runes': self.runes,
            'champion_items': self.champion_items,
            'lol_version': self.lol_version,
        }

    @staticmethod
    def get_queryset():
        videos = YtVideoDocument.search()
        video_list = [hit.serialize() for hit in videos]
        return video_list


class YtVideoDocumentSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    description = serializers.CharField()
    video_url = serializers.CharField()
    published_at = serializers.DateTimeField()
    champion = serializers.CharField()
    opponent_champion = serializers.CharField()
    lane = serializers.CharField()
    runes = serializers.ListSerializer(child=serializers.CharField())
    champion_items = serializers.ListSerializer(child=serializers.CharField())
    lol_version = serializers.CharField()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        elastic_id = instance.meta.id
        repr['id'] = elastic_id
        return repr

    def create(self, validated_data):
        del validated_data['id']
        ytvideo = YtVideoDocument(**validated_data)
        result = ytvideo.save(return_doc_meta=True)
        meta_id = result.body.get("_id")
        ytvideo.meta.id = meta_id
        ytvideo.id = meta_id
        return ytvideo
