from businesslogic.data_extraction import find_lane_from_string, find_champion_from_string


class TestBusinessLogic:
    def test_find_lane_from_string(self):
        description = "The SECRET KOREAN SUPPORT that can carry every game..."
        assert find_lane_from_string(description) == "Support"

        description = "volibear toplane gameplay"
        assert find_lane_from_string(description) == "Top"

        description = "volibear wherever gameplay"
        assert find_lane_from_string(description) is None

    def test_find_champion_from_string(self):
        description = "Rumble is the SECRET KOREAN SUPPORT that can carry every game..."
        assert find_champion_from_string(description) == "Rumble"

        description = "Camille is back with a brand new Support Item"
        assert find_champion_from_string(description) == "Camille"

        description = "brand new Support Item video"
        assert find_champion_from_string(description) is None
