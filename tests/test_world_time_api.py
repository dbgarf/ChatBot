from src.world_time_api import WorldTimeAPI

class TestWorldTimeAPI:

    def test_good_response(self, mock_good_response):
        api = WorldTimeAPI()
        result, message = api.get_time_at_timezone('America/Los_Angeles')
        assert result == True
        assert message == "18 Aug 2020 21:07"

    def test_invalid_timezone_response(self, mock_invalid_timezone_response):
        api = WorldTimeAPI()
        result, message = api.get_time_at_timezone('America')
        assert result == False
        assert message == 'Unknown Timezone'

    def test_not_found_response(self, mock_not_found_response):
        api = WorldTimeAPI()
        result, message = api.get_time_at_timezone('foobar')
        assert result == False
        assert message == 'Unknown Timezone'