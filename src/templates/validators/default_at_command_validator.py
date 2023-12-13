from ...models.commands.command_validator import CommandValidator

class DefaultATCommandValidator(CommandValidator):
    def validate(self, response, *args) -> bool:
        command = args[1]
        if response == "0#!#0":
            return False
        
        if response.find(command.command_text) != -1:
            return True