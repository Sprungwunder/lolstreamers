import os

from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
import ssl

api_key = os.getenv("YT_API_KEY")

YOUTUBE = None


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


def get_yt_connection():
    global YOUTUBE
    if api_key is None:
        raise ValueError("YouTube API key is missing")
    if YOUTUBE is None:
        # Configure SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        YOUTUBE = build('youtube', 'v3',
                        developerKey=api_key,
                        cache=MemoryCache(),
                        static_discovery=False)
    return YOUTUBE


"""
get the youtube video information for the given ID

json response example:
    
{'kind': 'youtube#videoListResponse', 
 'etag': 'JQMaWSbT0PhxTtk1k-Gts_mpwG0', 
 'items':     
    [{'kind': 'youtube#video', 'etag': 'b0i_5Mbhi4h-HGMoTjFyy1DkdO8', 'id': 'PDuIp8Y9aIY',
      'snippet': {'publishedAt': '2024-10-21T16:00:34Z', 
                  'channelId': 'UCcDZST9Rzue7gMruGN8CeIw',
                  'title': 'VOLIBEAR TOP IS THE #1 NEW 1V5 END BOSS IN SPLIT 3 (QUADRA KILL) - S14 Volibear TOP Gameplay Guide',
                  'description': "VOLIBEAR TOP IS THE #1 NEW 1V5 END BOSS IN SPLIT 3 (QUADRA KILL) - S14 Volibear TOP Gameplay Guide\nLeague of Legends Season 14 Volibear Toplane Gameplay Guide!\n#volibear #volibearguide #volibeargameplay \n\n🥇Toplane Tierlists & Coaching VODS\nhttps://www.patreon.com/Daveyx3\n\n🎮 TWITCH: https://www.twitch.tv/daveyx3\n🌍 DISCORD: https://discord.gg/t5WKfF7\n📷 INSTAGRAM: https://www.instagram.com/daveyx3/\n👔 MERCH STORE: https://daveyx3-shop.fourthwall.com/\n👉 2ND CHANNEL: https://bit.ly/daveyx3_offmeta\n\n💻 MY PC GEAR: https://www.amazon.com/shop/daveyx3 (Affiliate)\nIf you purchase anything from this link, I'll receive a small commission!\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\nSeason 14 Volibear Runes: \nExplained at beginning of the video.\n\nSeason 14 Volibear Build:\n(nashor tooth - mejai - rabadon - riftmaker - zhonya)\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n[Concepts of this video + Information + Everything you can find on my Channel]:\nLeague of Legends Gameplay Guides, League Gameplay Guides, LoL Gameplay Guides, League of Legends Guide, League Guide, LoL Guide, Season 14 Guide League of Legends, S14 Guide League of Legends, League of Legends Best Runes Season 14, League of Legends Best Build season 14, League of Legends Best Playstyle Season 14, Season 14 Tips, S14 Tips, League of Legends Tips, League of Legends, Daveyx3 Gameplay Channel.\nI'm a Challenger Top Main. Been challenger since S7/S8/S9/S10 & Season 11 and peaked 1109 LP at most. and I upload new video's everyday!",
                  'thumbnails': {
                      'default': {'url': 'https://i.ytimg.com/vi/PDuIp8Y9aIY/default.jpg', 'width': 120,
                                  'height': 90},
                      'medium': {'url': 'https://i.ytimg.com/vi/PDuIp8Y9aIY/mqdefault.jpg',
                                 'width': 320, 'height': 180},
                      'high': {'url': 'https://i.ytimg.com/vi/PDuIp8Y9aIY/hqdefault.jpg', 'width': 480,
                               'height': 360},
                      'standard': {'url': 'https://i.ytimg.com/vi/PDuIp8Y9aIY/sddefault.jpg',
                                   'width': 640, 'height': 480},
                      'maxres': {'url': 'https://i.ytimg.com/vi/PDuIp8Y9aIY/maxresdefault.jpg',
                                 'width': 1280, 'height': 720}}, 
                  'channelTitle': 'Daveyx3 Gameplay',
                  'tags': ['volibear', 'volibear lol', 'lol volibear', 'volibear league',
                           'volibear league of legends', 'volibear guide', 'volibear guide s14',
                           'volibear guide season 14', 'volibear top', 'volibear top guide',
                           'volibear top guide season 14', 'volibear gameplay', 'volibear gameplay s14',
                           'volibear gameplay season 14', 'how to play volibear', 'volibear combo',
                           'volibear runes', 'volibear build', 'volibear build s14',
                           'volibear build season 14', 'volibear top guide s14', 'volibear s14',
                           'daveyx3 gameplay', 'daveyx3', 'league of legends'], 
                  'categoryId': '20',
                  'liveBroadcastContent': 'none', 
                  'defaultLanguage': 'en', 
                  'localized': {
                    'title': 'VOLIBEAR TOP IS THE #1 NEW 1V5 END BOSS IN SPLIT 3 (QUADRA KILL) - S14 Volibear TOP Gameplay Guide',
                    'description': "VOLIBEAR TOP IS THE #1 NEW 1V5 END BOSS IN SPLIT 3 (QUADRA KILL) - S14 Volibear TOP Gameplay Guide\nLeague of Legends Season 14 Volibear Toplane Gameplay Guide!\n#volibear #volibearguide #volibeargameplay \n\n🥇Toplane Tierlists & Coaching VODS\nhttps://www.patreon.com/Daveyx3\n\n🎮 TWITCH: https://www.twitch.tv/daveyx3\n🌍 DISCORD: https://discord.gg/t5WKfF7\n📷 INSTAGRAM: https://www.instagram.com/daveyx3/\n👔 MERCH STORE: https://daveyx3-shop.fourthwall.com/\n👉 2ND CHANNEL: https://bit.ly/daveyx3_offmeta\n\n💻 MY PC GEAR: https://www.amazon.com/shop/daveyx3 (Affiliate)\nIf you purchase anything from this link, I'll receive a small commission!\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\nSeason 14 Volibear Runes: \nExplained at beginning of the video.\n\nSeason 14 Volibear Build:\n(nashor tooth - mejai - rabadon - riftmaker - zhonya)\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n[Concepts of this video + Information + Everything you can find on my Channel]:\nLeague of Legends Gameplay Guides, League Gameplay Guides, LoL Gameplay Guides, League of Legends Guide, League Guide, LoL Guide, Season 14 Guide League of Legends, S14 Guide League of Legends, League of Legends Best Runes Season 14, League of Legends Best Build season 14, League of Legends Best Playstyle Season 14, Season 14 Tips, S14 Tips, League of Legends Tips, League of Legends, Daveyx3 Gameplay Channel.\nI'm a Challenger Top Main. Been challenger since S7/S8/S9/S10 & Season 11 and peaked 1109 LP at most. and I upload new video's everyday!"
                   },
                   'defaultAudioLanguage': 'en'
      },
      'statistics': {'viewCount': '6584', 
                     'likeCount': '267', 
                     'favoriteCount': '0',
                     'commentCount': '37'}
    }]
}
"""


class YoutubeVideoInformation:
    def __init__(self, data: dict):
        if not data.get('items'):
            raise ValueError("No video information available")

        self._data = data['items'][0]
        self.title = self._data['snippet']['title']
        self.description = self._data['snippet']['description']
        self.views = self._data['statistics']['viewCount']
        self.likes = self._data['statistics']['likeCount']
        self.published_at = self._data['snippet']['publishedAt']
        self.channel = self._data['snippet']['channelTitle']


def get_yt_video_information(video_id: str) -> YoutubeVideoInformation:
    try:
        request = get_yt_connection().videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        return YoutubeVideoInformation(response)
    except ssl.SSLError:
        # Fallback with minimal information if YouTube API fails
        return YoutubeVideoInformation({
            'items': [{
                'snippet': {
                    'title': 'Unavailable',
                    'description': 'Video information temporarily unavailable',
                    'publishedAt': None,
                    'channelTitle': 'Unknown'
                },
                'statistics': {
                    'viewCount': '0',
                    'likeCount': '0'
                }
            }]
        })



def main():
    yt_video_information = get_yt_video_information("l_6I6LChDNk")
    print(yt_video_information.title)


if __name__ == "__main__":
    main()
