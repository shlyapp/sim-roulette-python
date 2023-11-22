from typing import List
from time import sleep
from threading import Thread

from .command import Command
from .command_status import CommandStatus
from .command_handler import macros_finish


class Macros():
    """Макрос, последовательный список команд на выполнение"""
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        """Список команд"""
        self.uuid = None
        """UUID"""
        self.command_answer = None
        """Ответ на выполнение макроса"""
        self.command = commands[-1]
        self.finish_event()

    @macros_finish()
    def finish_event(self) -> None:
        print("Macros has been complete")
    
    def is_finish(self) -> bool:
        if self.command_answer == None:
            return False
        if self.command_answer.message.find('complete') != -1:
            return True
        return False
