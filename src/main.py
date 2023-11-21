import logging

from .models.cell import Cell
from .models.command import Macros, COMMAND_EXECUTOR_THREAD, QUEUE_THREAD, Command, ATCommand
from .scripts import connect

logging.basicConfig(
    filename="sim-roulette-python/src/logs2.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def main():
    COMMAND_EXECUTOR_THREAD.start()
    macros = Macros([
        Command('card:A3'),
        Command('modem>connect'),
        Command('modem>on'),
        Command('modem>activation:bool'),
        ATCommand('AT+CMGR=1')
    ])
    
    macros.run()
    logging.info(macros.uuid)
    
    macros.run()
    logging.info(macros.uuid)
    
    while True:
        continue    
    
if __name__ == "__main__":
    main()
