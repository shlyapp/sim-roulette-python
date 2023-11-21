from typing import List

from .command import Command


class Macros():
    """Макрос, последовательный список команд на выполнение"""
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        """Список команд"""
        self.uuid = None
        """UUID"""
        self.command_answer = None
        """Ответ на выполнение макроса"""
