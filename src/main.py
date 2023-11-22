import logging

from .commands.command_pool import CommandPool
from .tools.macros import get_macros_connect
from .tools.commands.card import get_command_select_card
from .models.cell import Cell

logging.basicConfig(
    filename="sim-roulette-python/logs/logs.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

def main():
    command_pool = CommandPool()
    macros = get_macros_connect(Cell('A', 3))
    command_pool.add_command(macros)
    command = get_command_select_card(Cell('A', 3))
    command_pool.add_command(command)
    command_pool.start()
    
    while True:
        continue


if __name__ == "__main__":
    main()
