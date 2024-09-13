"""
Youtube Elasticsearch Documents Model
"""
from elasticsearch_dsl import Text, Date, Keyword, Document


class YtVideoDocument(Document):
    title = Text()
    description = Text()
    video_url = Text()
    published_at = Date()
    champion = Keyword()
    opponent_champion = Keyword()
    lane = Keyword()
    runes = Text()
    items = Text()
    lol_version = Keyword()

    class Index:
        name = 'lolstreamsearch_yt_videos'
        settings = {
            'number_of_shards': 1,
            'auto_expand_replicas': '0-1'
        }

    def prepare(self, instance):
        # Bereitet das Dokument zur Indizierung vor
        return {
            'title': instance.title,
            'description': instance.description,
            'video_url': instance.video_url,
            'published_at': instance.published_at,
            'champion': instance.champion,
            'opponent_champion': instance.opponent_champion,
            'lane': instance.lane,
            'runes': instance.runes,
            'items': instance.items,
            'lol_version': instance.lol_version,
        }
