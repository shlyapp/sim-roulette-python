import logging
from datetime import date

from .commands.command_pool import CommandPool
from .commands.macros import Macros
from .commands.command_handler import command_handler
from .commands.command_answer import CommandStatus
from .tools.macros import get_macros_number
from .tools.commands.card import get_command_select_card
from .models.cell import Cell
from .database.tools import get_command_answer


logging.basicConfig(
    filename=f"sim-roulette-python/logs/{date.today().strftime('%d-%m-%Y')}.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


command_pool = CommandPool()
macros = get_macros_number(Cell('A', 1))
command_pool.add_command(macros)
command_pool.start()

def main():
    handl()
    while True:
        continue


@command_handler(command=macros)
def handl(command):
    print("Задача сделана!")
    print(command.command_answer.message)
    

if __name__ == "__main__":
    main()
