import logging
import os
import re
import time
import socket

from django.core.validators import URLValidator
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from googleapiclient.errors import HttpError
import ssl

from rest_framework.exceptions import ValidationError

api_key = os.getenv("YT_API_KEY")

YOUTUBE = None
MAX_RETRIES = 3
TIMEOUT = 5  # seconds
BACKOFF_FACTOR = 2

logger = logging.getLogger(__name__)


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

def validate_youtube_url(url):
    logger.debug("Validating YouTube URL: %s", url)
    if not url or not isinstance(url, str):
        raise ValueError("Invalid URL type")

    # Trim whitespace
    url = url.strip()

    # Check maximum length (reasonable limit for YouTube URLs)
    if len(url) > 300:
        raise ValueError("URL is too long")

    # Validate URL format using Django's URLValidator
    url_validator = URLValidator(schemes=['http', 'https'])
    try:
        url_validator(url)
    except ValidationError:
        raise ValueError("Invalid URL format")

    # Case insensitive regex for YouTube-specific validation
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}([?&][^&\s]*)*$'

    if not re.match(youtube_regex, url, re.IGNORECASE):
        raise ValueError("Invalid YouTube URL format")

    # Ensure HTTPS in production
    if not url.startswith('https://'):
        url = url.replace('http://', 'https://')

    return url


def get_yt_id_and_timestamp(url, validate=False):
    """
    handles youtube video URL and returns the YouTube ID and timestamp
    two possible formats: https://youtu.be/Kryc40r9wOg?feature=shared&t=1737
    or:                   https://www.youtube.com/watch?v=Kryc40r9wOg&t=1737s

    :return:
    """
    logger.debug("Getting YouTube ID and timestamp from url: %s", url)
    timestamp = 0
    video_id = None

    try:
        if validate:
            url = validate_youtube_url(url)

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

        if not video_id or len(video_id) != 11:
            raise ValueError("Invalid YouTube video ID")

        return video_id, timestamp
    except (IndexError, KeyError):
        raise ValueError("Invalid YouTube URL structure")
    except ValueError as e:
        raise ValueError(str(e))

def get_yt_video_information(video_id: str) -> YoutubeVideoInformation:
    retry_count = 0
    last_exception = None
    logger.debug(f"Fetching video information for video ID: {video_id}")
    while retry_count < MAX_RETRIES:
        try:
            # Set timeout for this request
            socket.setdefaulttimeout(TIMEOUT)

            request = get_yt_connection().videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            logger.debug(f"Video information response: {response}")
            return YoutubeVideoInformation(response)
        except (ssl.SSLError, TimeoutError, HttpError) as e:
            logger.error(f"Error fetching video information: {str(e)}")
            last_exception = e
            retry_count += 1
            if retry_count < MAX_RETRIES:
                # Exponential backoff
                time.sleep(BACKOFF_FACTOR ** retry_count)
            continue
        except Exception as e:
            logger.error(f"Error fetching video information: {str(e)}")
            retry_count += 1
            last_exception = e
            pass
    # For any other unexpected errors, return minimal information
    return YoutubeVideoInformation({
        'items': [{
            'snippet': {
                'title': 'Unavailable',
                'description': f'Video information unavailable: {str(last_exception)}',
                'publishedAt': None,
                'channelTitle': 'Unknown'
            },
            'statistics': {
                'viewCount': '0',
                'likeCount': '0'
            }
        }]
    })

def extract_opgg_url_from_yt(yt_url: str) -> str:
    yt_id = get_yt_id_and_timestamp(yt_url, validate=True)[0]
    yt_video_information = get_yt_video_information(yt_id)

    opgg_pattern = r'https://op\.gg/lol/[^\s]+'

    try:
        match = re.search(opgg_pattern, yt_video_information.description)
        if match:
            return match.group(0)
        logger.debug("No op.gg URL found in video description")
        return ""
    except Exception as e:
        logger.error(f"Error extracting op.gg URL: {str(e)}")
        return ""


def main():
    yt_video_information = get_yt_video_information("l_6I6LChDNk")
    print(yt_video_information.title)


if __name__ == "__main__":
    main()
