from ...models.commands.command_validator import CommandValidator


class DefaultCommandValidator(CommandValidator):
    def validate(self, response, *args) -> bool:
        step = args[0]
        if response == "0#!#0":
            return False
        data = response.replace('#', '').split('!')

        if int(data[0]) == (step - 1):
            if int(data[1]) == 1:
                return True
        return False