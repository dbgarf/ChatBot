import pytest
from src.chatbot import ChatBot

def test_parse_command_good_input():
    chatbot = ChatBot()
    good_input = "dan: !timeat America/Los_Angeles"
    command, argument = chatbot.parse_command(good_input)
    assert command == 'timeat'
    assert argument == 'America/Los_Angeles'

def test_parse_command_bad_input():
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