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

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'published_at': self.published_at,
            'champion': self.champion,
            'opponent_champion': self.opponent_champion,
            'lane': self.lane,
            'runes': [ x for x in self.runes ],
            'items': [ x for x in self.items ],
            'lol_version': self.lol_version,
        }
