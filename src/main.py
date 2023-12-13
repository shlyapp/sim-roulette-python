from .models.commands.command import Command
from .models.commands.command_pool import CommandPool

from .templates.validators.validators import *

from .utils.logger import logger
from time import sleep


def main():
    logger.info("Start!")
        
    command_modem_connect = Command(
        command_text="modem>connect",
    )
    command_modem_on = Command(
        command_text="modem>on",
    )
    command_activation = Command(
        command_text="modem>activation:bool",
    )
    command_send = Command(
        command_text="AT+CMGR=1",
        validator=default_at_command_validator
    )
    command_pool = CommandPool()
    command_pool.start()
    for i in range(1, 10):
        command_connect = Command(
            command_text=f"card:B{i}",
        )
        command_pool.add_command(command_connect)
        command_pool.add_command(command_modem_connect)
        command_pool.add_command(command_modem_on)
        command_pool.add_command(command_activation)
        command_pool.add_command(command_send)


if __name__ == "__main__":
    main()    
