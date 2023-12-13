from ...models.commands.command_validator import CommandValidator
from time import sleep


class ModemActivationValidator(CommandValidator):
    def validate(self, response, *args) -> bool:
        step = args[0]
        if response == "0#!#0":
            return False
        data = response.replace('#', '').split('!')

        sleep(20)
        
        if int(data[0]) == (step - 1):
            if int(data[1][0]) == 1:
                return True
        return False