from queue import Queue, Empty
from typing import cast
from threading import Thread

from .macros import Macros
from .command import Command
from .command_answer import *


class CommandPool():
    def __init__(self) -> None:
        self._thread = Thread(
            target=self._command_executor,
            daemon=True
        )
        self._queue = Queue()
    
    def _command_executor(self) -> None:
        while True:
            try:
                item = self._queue.get()

                if isinstance(item, Macros):
                    macros = cast(Macros, item)
                    for command in macros.commands:
                        run_command(command)
                        command.command_answer.status = CommandStatus.in_progress
                else:
                    command = cast(Command, item)
                    command.command_answer.status = CommandStatus.in_progress
                    run_command(command)
            except Empty:
                pass


    def add_command(self, item) -> uuid.UUID:
        item.uuid = uuid.uuid4()
        item.command_answer = CommandAnswer(uuid=item.uuid)
        self._queue.put(item)
        return item.uuid

    def start(self) -> None:
        self._thread.start()
