from .models.commands.command import Command
from .models.commands.command_pool import CommandPool

from .templates.validators.default_validator import DefaultCommandValidator
from .templates.callbacks.default_callback import DefaultCommandCallback

from .utils.logger import logger

def main():
    command_connect = Command(
        command_text="card:B10",
    )
    command_modem_connect = Command(
        command_text="modem>connect",
    )
    command_modem_on = Command(
        command_text="modem>on",
    )
    command_pool = CommandPool()
    command_pool.add_command(command_connect)
    command_pool.add_command(command_modem_connect)
    command_pool.add_command(command_modem_on)
    command_pool.start()
    
    
if __name__ == "__main__":
    main()    