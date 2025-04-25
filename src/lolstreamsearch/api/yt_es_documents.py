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
from elasticsearch_dsl import Text, Date, Keyword, Document, Boolean
from rest_framework import serializers

from google_api import get_yt_video_information


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
    team_champions = Keyword()
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
        videos = YtVideoDocument.search()
        for key, values in query_params.items():
            if values == "":
                continue
            for value in values.split(","):
                if key in ["lane", "is_active"]:
                    videos = videos.filter("term", **{key: value})
                else:
                    videos = videos.filter("term", **{key+".keyword": value})
        video_list = [hit.serialize() for hit in videos]
        return video_list

    def set_active_and_serialize(self, is_active=True):
        self.update(is_active=is_active)
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

    def get_yt_id_and_timestamp(self, instance):
        """
        handles youtube video URL and returns the YouTube ID and timestamp
        two possible formats: https://youtu.be/Kryc40r9wOg?feature=shared&t=1737
        or:                   https://www.youtube.com/watch?v=Kryc40r9wOg&t=1737s

        :return:
        """
        
        timestamp = 0
        video_id = None
        try:
            url = instance["video_url"]
            if "youtu.be" in url:
                # Handle short format
                path = url.split("youtu.be/")[1]
                video_id = path
                if "?" in path:
                    video_id = path.split("?")[0]
                    query_params = path.split("?")[1]
                    for param in query_params.split("&"):
                        if param.startswith("t="):
                            timestamp = param.split("=")[1].rstrip("s")

            else:
                # Handle long format
                query_params = url.split("?", 1)[1]
                for param in query_params.split("&"):
                    if param.startswith("v="):
                        video_id = param.split("=")[1]
                    elif param.startswith("t="):
                        timestamp = param.split("=")[1].rstrip("s")

            if not video_id:
                raise ValueError("Could not extract video ID from URL")

            return video_id, timestamp
        except (IndexError, KeyError, ValueError):
            raise ValueError("Invalid YouTube video URL provided.")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, YtVideoDocument):
            representation['id'] = instance.meta.id

        representation['ytid'], representation['timestamp'] = self.get_yt_id_and_timestamp(instance)
        yt_info = get_yt_video_information(representation['ytid'])
        representation['views'] = yt_info.views
        representation['likes'] = yt_info.likes
        return representation

    def create(self, validated_data):
        if 'id' in validated_data:
            del validated_data['id']
        ytid , timestamp = self.get_yt_id_and_timestamp(validated_data)
        yt_video_info = get_yt_video_information(ytid)
        validated_data['ytid'] = ytid
        validated_data['timestamp']  = timestamp
        validated_data['title'] = yt_video_info.title
        validated_data['description'] = yt_video_info.description
        validated_data['published_at'] = yt_video_info.published_at
        validated_data['streamer'] = yt_video_info.channel
        validated_data['is_active'] = False
        ytvideo = YtVideoDocument(**validated_data)
        result = ytvideo.save(return_doc_meta=True)
        meta_id = result.body.get("_id")
        ytvideo.meta.id = meta_id
        ytvideo.id = meta_id
        return ytvideo


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
