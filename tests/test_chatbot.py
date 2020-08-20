import pytest
from src.chatbot import ChatBot
# from src import redis_client

# class MockRedis:
#     def __init__():
#         self.data = {}

#     def get(key):
#         return self.data.get(key)

#     def set(key, val):
#         self.data[key] = val

# @pytest.fixture
# def mock_redis(monkeypatch):

#     def mock_r:
#         return MockRedis()

#     monkeypatch.setattr(redis_client, "get_redis_client", mock_r)

class TestChatbot:

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

    def test_increments_count_on_valid_request(self, mock_redis, mock_good_response):
        chatbot = ChatBot()
        # make a first request
        result = chatbot.handle_message('dan: !timeat America/Los_Angeles')
        assert result == "18 Aug 2020 21:07"
        # then check its popularity
        result = chatbot.handle_message('dan: !timepopularity America/Los_Angeles')
        assert int(result) == 1
        
