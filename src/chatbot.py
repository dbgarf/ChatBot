
import re

class ChatBot:

    def parse_command(self, input_message):
        "parses input message into command and argument"

        input_pattern = r'^(?P<username>\w+): (?P<message>.+)$'
        input_matches = re.match(input_pattern, input_message)
        if input_matches:
            username = input_matches.groupdict().get('username')
            message = input_matches.groupdict().get('message')
        else:
            return False
        
        message_pattern = r'^!(?P<command>\w+) (?P<argument>.+)$' # deliberately unspecific pattern, will check validity elsewhere
        if message:
            message_matches = re.match(message_pattern, message)

        if message_matches:
            command = message_matches.groupdict().get('command')
            argument = message_matches.groupdict().get('argument')
        else:
            return False

        return (command, argument)


