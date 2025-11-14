import re
from email.utils import unquote

from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

api_key = 'RGAPI-aec50855-7d77-42fa-bbf2-a741fd863174'

europe_endpoint = 'https://europe.api.riotgames.com'

headers = {
    'X-Riot-Token': settings.RIOT_API_KEY
}

def get_summoner_puuid(game_name, tag_line):
    logger.debug(f'Getting puuid for {game_name} {tag_line}')
    account_response = requests.get(
        f'{europe_endpoint}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}',
        headers=headers
    )
    puuid = account_response.json()['puuid']
    logger.debug(f'Got puuid: {puuid}')
    return puuid


def get_match_by_id(match_id: str, region: str = 'europe') -> dict:
    """
    Get detailed match information by match ID

    Args:
        match_id: Match ID (format: EUW1_1234567890 or just the numeric part)
        region: Routing value (europe, americas, asia, sea)

    Returns:
        Dict with complete match data
    """
    # Ensure match_id has the region prefix
    if not match_id.startswith(
            ('EUW1_', 'EUN1_', 'NA1_', 'KR_', 'BR1_', 'JP1_',
             'LA1_', 'LA2_', 'OC1_', 'TR1_', 'RU_')):
        match_id = f'EUW1_{match_id}'

    logger.debug(f'Getting match data for {match_id}')
    response = requests.get(
        f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}',
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def parse_opgg_match_url(opgg_url: str) -> dict | None:
    """
    Extract platform region, Riot ID (gameName, tagLine) and timestamp from an op.gg URL.
    Example:
      https://op.gg/lol/summoners/euw/Chamkin-EUW/matches/<opaque>/1762466711000
    Returns: {'platform': 'euw', 'game_name': 'Chamkin', 'tag_line': 'EUW', 'timestamp': 1762466711000}
    """
    m = re.search(r'/summoners/([^/]+)/([^/]+)/matches/[^/]+/(\d+)', opgg_url)
    if not m:
        return None
    platform = m.group(1)
    riot_id = unquote(m.group(2))  # e.g. "Chamkin-EUW"
    ts_ms = int(m.group(3))
    # Riot ID part may use '-' between gameName and tagLine on op.gg
    if '-' in riot_id:
        game_name, tag_line = riot_id.rsplit('-', 1)
    else:
        # Fallback: if no '-', try decode with '#', else treat all as game_name
        parts = riot_id.split('#', 1)
        game_name = parts[0]
        tag_line = parts[1] if len(parts) > 1 else ''
    return {
        'platform': platform,
        'game_name': game_name,
        'tag_line': tag_line,
        'timestamp': ts_ms
    }

def get_matches_by_timestamp_range(puuid: str, start_time: int, end_time: int,
                                   region: str = 'europe', count: int = 100) -> list:
    """
    Get matches within a specific timestamp range

    Args:
        puuid: Player PUUID
        start_time: Start timestamp in seconds (epoch)
        end_time: End timestamp in seconds (epoch)
        region: Routing value
        count: Max number of matches to retrieve (max 100)

    Returns:
        List of match IDs
    """
    logger.debug(f'Getting matches for {puuid} between {start_time} and {end_time}')
    response = requests.get(
        f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids',
        headers=headers,
        params={
            'startTime': start_time,
            'endTime': end_time,
            'count': count
        }
    )
    response.raise_for_status()
    return response.json()


def get_participant_data(match_data: dict, puuid: str) -> dict | None:
    for participant in match_data['info']['participants']:
        if participant['puuid'] == puuid:
            return participant
    return None

def get_match_info_for_player(match_data: dict, puuid: str) -> dict | None:
    enriched_participant_data = get_participant_data(match_data, puuid)
    if enriched_participant_data is None:
        return None
    for item in ["item0", "item1", "item2", "item3", "item4", "item5"]:
        enriched_participant_data[item] = get_item_name(enriched_participant_data[item])

    rune_data = get_rune_information(enriched_participant_data)
    enriched_participant_data.update(rune_data)

    return enriched_participant_data

def get_rune_information(participant_data) -> dict:
    """
        Extract runes information from participant data

        Returns:
            Dict with primary and secondary rune information
        """
    perks = participant_data.get('perks', {})

    # Get the styles (Primary and Secondary rune trees)
    styles = perks.get('styles', [])

    primary_style = styles[0] if len(styles) > 0 else {}
    secondary_style = styles[1] if len(styles) > 1 else {}

    # Extract primary runes (keystone + 3 other runes)
    primary_selections = primary_style.get('selections', [])
    primary_runes = [selection['perk'] for selection in primary_selections]

    # Extract secondary runes (2 runes)
    secondary_selections = secondary_style.get('selections', [])
    secondary_runes = [selection['perk'] for selection in secondary_selections]

    return {
        'primary_style': primary_style.get('style'),  # Tree ID (e.g., 8000 for Precision)
        'primary_runes': [get_rune_name(rune_id) for rune_id in primary_runes],  # [keystone, rune1, rune2, rune3]
        'secondary_style': secondary_style.get('style'),  # Tree ID
        'secondary_runes': [get_rune_name(rune_id) for rune_id in secondary_runes],
        'stat_perks': {
            'offense': perks.get('statPerks', {}).get('offense'),
            'flex': perks.get('statPerks', {}).get('flex'),
            'defense': perks.get('statPerks', {}).get('defense')
        }
    }


# Cache for static data
_items_cache = None
_runes_cache = None
_latest_version = None


def get_latest_version():
    """Get the latest League of Legends version"""
    global _latest_version
    if _latest_version is None:
        response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
        versions = response.json()
        _latest_version = versions[0]
    return _latest_version


def get_items_data():
    """Fetch and cache items data from Data Dragon"""
    global _items_cache
    if _items_cache is None:
        version = get_latest_version()
        response = requests.get(
            f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json'
        )
        data = response.json()
        _items_cache = data['data']
    return _items_cache


def get_runes_data():
    """Fetch and cache runes data from Data Dragon"""
    global _runes_cache
    if _runes_cache is None:
        version = get_latest_version()
        response = requests.get(
            f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json'
        )
        _runes_cache = response.json()
    return _runes_cache


def get_item_name(item_id: int) -> str:
    """
    Get item name from item ID

    Args:
        item_id: Item ID from match data

    Returns:
        Item name or "Unknown Item" if not found
    """
    if item_id == 0:
        return None

    items = get_items_data()
    item_str = str(item_id)

    if item_str in items:
        return items[item_str]['name']

    return f"Unknown Item ({item_id})"


def get_rune_name(rune_id: int) -> str:
    """
    Get rune name from rune ID

    Args:
        rune_id: Rune ID from match data

    Returns:
        Rune name or "Unknown Rune" if not found
    """
    runes_data = get_runes_data()

    # Search through all rune trees and slots
    for tree in runes_data:
        # Check if it's a tree/style ID
        if tree['id'] == rune_id:
            return tree['name']

        # Check slots for individual runes
        for slot in tree['slots']:
            for rune in slot['runes']:
                if rune['id'] == rune_id:
                    return rune['name']

    return f"Unknown Rune ({rune_id})"


def extract_from_opgg(opgg_url: str) -> dict | None:
    """
    given the op.gg url extract the summoner information and timestamps to
    find the corresponding match and extract the match data
    :param opgg_url: op.gg game url
    :returns: player data dict
    """
    parsed_url = parse_opgg_match_url(opgg_url)
    if parsed_url is None:
        logger.debug(f"Invalid URL {opgg_url}")
        return None
    puuid = get_summoner_puuid(parsed_url['game_name'], parsed_url['tag_line'])
    time_start = int(parsed_url['timestamp']/1000)
    # 5 minute time window
    matches = get_matches_by_timestamp_range(puuid, time_start, time_start+300)
    if len(matches) == 0:
        logger.debug("No matches found")
        return None
    logger.debug(f"Found {len(matches)} matches: {matches}")
    match_id = matches[0]
    match_data = get_match_by_id(match_id)
    player_data = get_match_info_for_player(match_data, puuid)
    return player_data
