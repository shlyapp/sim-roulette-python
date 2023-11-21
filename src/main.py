import logging

from .models.commands.command_pool import CommandPool
from .models.commands.command import Command


logging.basicConfig(
    filename="sim-roulette-python/src/logs2.log",
    filemode="a",
    encoding="utf-8",
    format="%command_status(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def main():
    command_pool = CommandPool()
    command = Command("hello")
    print(command.uuid)
    print(command.command_answer)
    answer = command_pool.add_command_in_queue(command)
    print(command.command_answer.status)    
    command_pool.start()

    print(command.command_answer.status)    

if __name__ == "__main__":
    main()
