"""
Youtube Elasticsearch Documents Model


POST:

{
  "video_url": "https://www.youtube.com/watch?v=uZeMAnXhoIU&t=1774s",
  "champion": "Yorick",
  "enemy_champion": "Nocturne",
  "team_champions": [
    "Cho'Gath", "Xerath", "Ezreal", "Lulu"
  ],
  "enemy_team_champions": [
    "Pantheon", "Kassadin", "Kai'Sa","Rakan"
  ],
  "lane": "Jungle",
  "runes": [
    "Conqueror", "Triumph", "Legend: Alacrity", "Coup de Grace", "Magical Footwear", "Approach Velocity"
  ],
  "champion_items": [
    "Trinity Force", "Spear of Shojin", "Plated Steelcaps", "Sterak's Gage", "Spirit Visage", "Death's Dance"
  ],
  "lol_version": "15"
}


"""
import logging

import urllib3
from elasticsearch_dsl import Text, Date, Keyword, Document, Boolean
from rest_framework import serializers

from google_api import get_yt_video_information, get_yt_id_and_timestamp
from lolstreamers import settings

if settings.DEBUG:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class YtVideoDocument(Document):
    id = Keyword()
    ytid = Text()
    timestamp = Text()
    title = Text()
    description = Text()
    video_url = Text()
    published_at = Date()
    champion = Keyword()
    enemy_champion = Keyword()
    team_champions = Keyword(multi=True)
    enemy_team_champions = Keyword(multi=True)
    lane = Keyword()
    runes = Keyword(multi=True)
    champion_items = Keyword(multi=True)
    lol_version = Keyword()
    streamer = Keyword()
    is_active = Boolean()

    class Index:
        name = 'lolstreamsearch_yt_videos'
        settings = {
            'number_of_shards': 1,
            'auto_expand_replicas': '0-1'
        }

    def serialize(self):
        return {
            'id': self.meta.id,
            'ytid': self.ytid,
            'timestamp': self.timestamp,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'published_at': self.published_at,
            'champion': self.champion,
            'enemy_champion': getattr(self, "enemy_champion", ''),
            'team_champions': getattr(self, "team_champions", []),
            'enemy_team_champions': self.enemy_team_champions,
            'lane': self.lane,
            'runes': self.runes,
            'champion_items': self.champion_items,
            'lol_version': self.lol_version,
            'streamer': self.streamer,
            'is_active': self.is_active
        }

    # simple example request
    # ...ytvideos/?champion=Volibear&lane=&opponent_champion=&runes=Press%20the%20Attack&team_champions=Neeko%2CEzreal%2CPoppy%2CVayne
    @staticmethod
    def get_queryset(query_params):
        logger.debug("Querying Youtube videos with query params: %s", query_params)
        videos = YtVideoDocument.search()
        videos = videos.sort("-published_at")
        for key, values in query_params.items():
            if values == "":
                continue
            values_list = values.split(",")
            if key == "streamer":
                # Create a bool query with should clauses for multiple streamers
                should_clauses = []
                for value in values_list:
                    should_clauses.append({"term": {"streamer": value}})
                videos = videos.query("bool", should=should_clauses)
            elif key in ["lane", "is_active", "lol_version"]:
                videos = videos.filter("term", **{key: values})
            else:
                for value in values_list:
                    videos = videos.filter("term", **{key + ".keyword": value})

        logger.debug(f"videos.to_dict(): {videos.to_dict()}")
        logger.debug("Found %s videos", videos.count())
        video_list = [hit.serialize() for hit in videos]
        return video_list

    def set_active_and_serialize(self, is_active=True):
        logger.debug("Setting Youtube video %s to active: %s", self.meta.id, is_active)
        self.update(is_active=is_active, refresh=True)
        return self.serialize()


class YtVideoDocumentSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    ytid = serializers.CharField(required=False)
    timestamp = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    video_url = serializers.CharField()
    published_at = serializers.DateTimeField(required=False)
    champion = serializers.CharField()
    enemy_champion = serializers.CharField()
    team_champions = serializers.ListField(child=serializers.CharField())
    enemy_team_champions = serializers.ListSerializer(child=serializers.CharField())
    lane = serializers.CharField()
    runes = serializers.ListSerializer(child=serializers.CharField())
    champion_items = serializers.ListSerializer(child=serializers.CharField())
    lol_version = serializers.CharField()
    streamer = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    views = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, YtVideoDocument):
            representation['id'] = instance.meta.id

        representation['ytid'], representation['timestamp'] = get_yt_id_and_timestamp(instance['video_url'])
        yt_info = get_yt_video_information(representation['ytid'])
        representation['views'] = yt_info.views
        representation['likes'] = yt_info.likes
        return representation

    def _set_validated_data(self, validated_data):
        ytid, timestamp = get_yt_id_and_timestamp(validated_data['video_url'], validate=True)
        yt_video_info = get_yt_video_information(ytid)
        validated_data['ytid'] = ytid
        validated_data['timestamp'] = timestamp
        validated_data['title'] = yt_video_info.title
        validated_data['description'] = yt_video_info.description
        validated_data['published_at'] = yt_video_info.published_at
        validated_data['streamer'] = yt_video_info.channel

    def _save(self, validated_data):
        ytvideo = YtVideoDocument(**validated_data)
        result = ytvideo.save(return_doc_meta=True, refresh=True)
        meta_id = result.body.get("_id")
        ytvideo.meta.id = meta_id
        ytvideo.id = meta_id
        return ytvideo

    def create(self, validated_data):
        if 'id' in validated_data:
            del validated_data['id']
        self._set_validated_data(validated_data)
        validated_data['is_active'] = False
        return self._save(validated_data)

    def update(self, instance, validated_data):
        self._set_validated_data(validated_data)
        validated_data['_id'] = instance.meta.id
        return self._save(validated_data)


class ChampionKeywordSerializer(serializers.Serializer):
    champion = serializers.ListSerializer(child=serializers.CharField())


class EnemyChampionKeywordSerializer(serializers.Serializer):
    enemy_champion = serializers.ListSerializer(child=serializers.CharField())


class RunesKeywordSerializer(serializers.Serializer):
    runes = serializers.ListSerializer(child=serializers.CharField())


class ItemsKeywordSerializer(serializers.Serializer):
    items = serializers.ListSerializer(child=serializers.CharField())


class TeamChampionKeywordSerializer(serializers.Serializer):
    team_champions = serializers.ListSerializer(child=serializers.CharField())


class EnemyTeamChampionKeywordSerializer(serializers.Serializer):
    enemy_team_champions = serializers.ListSerializer(child=serializers.CharField())

class StreamerKeywordSerializer(serializers.Serializer):
    streamer = serializers.ListSerializer(child=serializers.CharField())
