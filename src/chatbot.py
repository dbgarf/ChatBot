
import re

from src.commands import timeat, timepopularity

class UndefinedCommandError(Exception):
    pass

class ChatBot:

    # this could be done with a Registry decorator instead but that's more complicated than needed
    # for now stupid and simple is better, registry decorator more sensible for larger code base
    COMMANDS = {
        'timeat': timeat,
        'timepopularity': timepopularity
    }

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


    def dispatch(self, command, argument):
        fn = self.COMMANDS.get(command)
        if fn:
            return fn(argument)

        raise UndefinedCommandError("Command with name: %s not found" % command)

    def handle_message(self, input_message):
        "primary public interface"

        result = self.parse_command(input_message)
        if result:
            command, argument = result
            return self.dispatch(command, argument)

        return "Couldn't figure out what to do with input message: %s" % input_message