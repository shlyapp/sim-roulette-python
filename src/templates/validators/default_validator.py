from ...models.commands.command_validator import CommandValidator
from ...models.commands.types.command_status import CommandStatus


class DefaultCommandValidator(CommandValidator):
    def validate(self, command) -> bool:
        message = command.command_answer.message
        if int(message[1]) == 1:
            return True
        return False