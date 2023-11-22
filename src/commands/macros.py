from typing import List

from .command import Command
from .command_status import CommandStatus


class Macros():
    """Макрос, последовательный список команд на выполнение"""
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        """Список команд"""
        self.uuid = None
        """UUID"""
        self.command_answer = None
        """Ответ на выполнение макроса"""
        
    def is_finish(self) -> bool:
        if self.command_answer == None:
            return False
        if self.command_answer.message.find('complete') != -1:
            return True
        return False
