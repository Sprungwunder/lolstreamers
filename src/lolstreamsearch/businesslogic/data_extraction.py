"""
This module contains functions for extracting data from various sources related to League of Legends (LoL) streams and videos.
"""
import re

from google_api import get_yt_id_and_timestamp, get_yt_video_information

CHAMPIONS_LIST = [
    'Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Ambessa', 'Amumu', 'Anivia', 'Annie',
    'Aphelios',
    'Ashe', 'Aurelion Sol', 'Aurora', 'Azir', 'Bard', 'Bel\'Veth', 'Blitzcrank', 'Brand', 'Braum',
    'Briar', 'Caitlyn', 'Camille', 'Cassiopeia', 'Cho\'Gath', 'Corki', 'Darius', 'Diana',
    'Dr. Mundo', 'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora',
    'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim',
    'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce',
    'Jhin', 'Jinx', 'K\'Sante', 'Kai\'Sa', 'Kalista', 'Karma', 'Karthus', 'Kassadin',
    'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Kha\'Zix', 'Kindred', 'Kled', 'Kog\'Maw',
    'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite',
    'Malzahar', 'Maokai', 'Master Yi', 'Mel', 'Milio', 'Miss Fortune', 'Mordekaiser', 'Morgana',
    'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu Willump',
    'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan',
    'Rammus', 'Rek\'Sai', 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble',
    'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana',
    'Singed', 'Sion', 'Sivir', 'Skarner', 'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra',
    'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle',
    'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar',
    'Vel\'Koz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Wukong',
    'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yunara', 'Yuumi', 'Zaahen', 'Zac',
    'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra'
]


def find_lane_from_string(description: str) -> str | None:
    lane_pattern = r'(top|mid|jungle|bot|adc|support)'
    match = re.search(lane_pattern, description, re.IGNORECASE)
    if match:
        return match.group(1).lower().capitalize()
    return None


def find_champion_from_string(description: str) -> str | None:
    for champion in CHAMPIONS_LIST:
        match = re.search(re.escape(champion), description)
        if match:
            return champion
    return None


def extract_from_yt_information(yt_url: str) -> dict | None:
    yt_id = get_yt_id_and_timestamp(yt_url, validate=True)[0]
    yt_video_information = get_yt_video_information(yt_id)

    lane = (find_lane_from_string(yt_video_information.title) or
            find_lane_from_string(yt_video_information.description))

    champion = (find_champion_from_string(yt_video_information.title) or
                find_champion_from_string(yt_video_information.description))

    if lane or champion:
        player_match_data = {
            'individualPosition': lane,
            'championName': champion,
        }
        return player_match_data

    return None
