from typing import List

from .command import Command
from .command_answer import CommandAnswer


class Macros():
    def __init__(self, commands: List[Command]):
        self.commands = commands
        self.uuid = None
        self.command_answer = None
