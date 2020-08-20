import pytest
from src.chatbot import ChatBot
from src.redis_client import get_redis_client

class TestChatbot:
    def setup(self):
        r = get_redis_client()
        r.flushall()

    def test_parse_command_good_input(self):
        chatbot = ChatBot()
        good_input = "dan: !timeat America/Los_Angeles"
        command, argument = chatbot.parse_command(good_input)
        assert command == 'timeat'
        assert argument == 'America/Los_Angeles'

    def test_parse_command_bad_input(self):
        chatbot = ChatBot()

        # gibberish
        result = chatbot.parse_command('gibberish')
        assert result == False

        # missing username
        result = chatbot.parse_command('!timeat America/Los_Angeles')
        assert result == False

        # missing message
        result = chatbot.parse_command('dan: ')
        assert result == False

        # missing !
        result = chatbot.parse_command('dan: timeat America/Los_Angeles')
        assert result == False

        # missing command
        result = chatbot.parse_command('dan: America/Los_Angeles')
        assert result == False

        # missing argument
        result = chatbot.parse_command('dan: !timeat')
        assert result == False

    def test_increments_count_on_valid_request(self, mock_good_response):
        chatbot = ChatBot()
        # make a first request
        result = chatbot.handle_message('dan: !timeat America/Los_Angeles')
        assert result == "18 Aug 2020 21:07"
        # then check its popularity
        result = chatbot.handle_message('dan: !timepopularity America/Los_Angeles')
        assert int(result) == 1

        # then do another and confirm it increments
        chatbot.handle_message('dan: !timeat America/Los_Angeles')
        result = chatbot.handle_message('dan: !timepopularity America/Los_Angeles')
        assert int(result) == 2

    def test_does_not_increment_count_on_invalid_request(self, mock_invalid_timezone_response):
        chatbot = ChatBot()
        # make an invalid request
        result = chatbot.handle_message('dan: !timeat America/LosT_Angeles')
        assert result == "Unknown Timezone"
        # then check its popularity, should be 0, we don't record invalid ones
        result = chatbot.handle_message('dan: !timepopularity America/LosT_Angeles')
        assert int(result) == 0

    def test_timepopularity_sums_prefix_matches(self):
        # going to directly set some keys in redis for purposes of this test, to simulate a history of previous valid requests
        r = get_redis_client()
        r.set('America/Los_Angeles', 1)
        r.set('America/Argentina/Buenos_Aires', 1)
        r.set('America/Argentina/Catamarca', 2)
        r.set('Europe/Paris', 3)
        r.set('Europe/London', 2)

        chatbot = ChatBot()
        result = chatbot.handle_message('dan: !timepopularity America')
        assert int(result) == 4

        result = chatbot.handle_message('dan: !timepopularity America/Argentina')
        assert int(result) == 3

        result = chatbot.handle_message('dan: !timepopularity Europe')
        assert int(result) == 5

        # and for good measure lets confirm that exact matches still work, and zero matches are still 0
        result = chatbot.handle_message('dan: !timepopularity America/Argentina/Buenos_Aires')
        assert int(result) == 1

        result = chatbot.handle_message('dan: !timepopularity Asia')
        assert int(result) == 0
