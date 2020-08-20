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
        
