from api.league import get_summoner_puuid, get_match_info_for_player, \
    get_rune_information, get_matches_by_timestamp_range, \
    parse_opgg_match_url, get_match_by_id, extract_from_opgg
from test_api.api_datasets import match_data, puuid


class TestLeagueApi:
    opgg_url = "https://op.gg/lol/summoners/euw/Chamkin-EUW/matches/KqFazGhft1WJ367iLRId1hqUYUZqfg9O20CuUS8cvCI%3D/1762466711000"

    def test_get_summoner_name(self):
        name = get_summoner_puuid("Chamkin", "EUW")
        assert name == puuid

    def test_parse_opgg_match_url(self):
        parsed_url_data = parse_opgg_match_url(self.opgg_url)
        assert parsed_url_data['platform'] == "euw"
        assert parsed_url_data['tag_line'] == "EUW"
        assert parsed_url_data['game_name'] == "Chamkin"
        assert parsed_url_data['timestamp'] == 1762466711000

    def test_get_matches_by_timestamp_range(self):
        start_time = 1762466711
        end_time = 1762466711
        matches = get_matches_by_timestamp_range(puuid, start_time, end_time + 300)
        assert len(matches) == 1
        assert matches[0] == 'EUW1_7594636490'

    def test_get_match_by_id(self):
        match_id = "EUW1_7594636490"
        match_data = get_match_by_id(match_id)
        assert 'info' in match_data

    def test_get_rune_information(self):
        runes = get_rune_information(match_data['info']['participants'][0])
        assert runes['primary_runes'] == ['Arcane Comet', 'Manaflow Band', 'Transcendence',
                                          'Gathering Storm']
        assert runes['secondary_runes'] == ['Biscuit Delivery', 'Magical Footwear']

    def test_get_match_info_for_player(self):
        player_info = get_match_info_for_player(match_data, puuid)
        assert player_info is not None
        assert player_info['riotIdGameName'] == "Chamkin"
        assert player_info['riotIdTagline'] == "EUW"

        # champion name, lane, items, runes
        assert player_info['championName'] == "Yorick"
        assert player_info['lane'] == "TOP"
        assert player_info['item0'] == "Doran's Ring"
        assert player_info['item1'] == "Liandry's Torment"
        assert player_info['item5'] is None
        assert player_info['primary_runes'] == ['Arcane Comet', 'Manaflow Band', 'Transcendence',
                                                'Gathering Storm']
        assert player_info['secondary_runes'] == ['Biscuit Delivery', 'Magical Footwear']

    def test_extract_from_opgg(self):
        player_match_data = extract_from_opgg(self.opgg_url)
        assert player_match_data is not None
        assert player_match_data['riotIdGameName'] == "Chamkin"
        assert player_match_data['riotIdTagline'] == "EUW"

        # champion name, lane, items, runes
        assert player_match_data['championName'] == "Yorick"
        assert player_match_data['lane'] == "TOP"
        assert player_match_data['item0'] == "Doran's Ring"
        assert player_match_data['item1'] == "Liandry's Torment"
        assert player_match_data['item5'] is None
        assert player_match_data['primary_runes'] == ['Arcane Comet', 'Manaflow Band',
                                                      'Transcendence',
                                                      'Gathering Storm']
        assert player_match_data['secondary_runes'] == ['Biscuit Delivery', 'Magical Footwear']
