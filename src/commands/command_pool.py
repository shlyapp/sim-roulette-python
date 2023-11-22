import logging

from queue import Queue, Empty
from typing import cast
from threading import Thread
from typing import cast

from .macros import Macros
from .command import Command
from .command_answer import *

# from ..database.tools import save_command_answer


class CommandPool():
    """Пул команд на выполнение"""
    def __init__(self) -> None:
        self._thread = Thread(
            target=self._command_executor,
            daemon=True
        )
        self._queue = Queue()
    
    def _command_executor(self) -> None:
        """Обработчик выполнений"""
        while True:
            try:
                item = self._queue.get()
                command = cast(Command, item)
                command.command_answer.status = CommandStatus.in_progress
                run_command(command)
            except Empty:
                pass

    def _assigns_uuid(self, item) -> uuid.UUID:
        if isinstance(item, Command):
            command = cast(Command, item)
            command.uuid = uuid.uuid4()
            command.command_answer = CommandAnswer(uuid=item.uuid)
            # save_command_answer(command)
        else:
            macros = cast(Macros, item)
            macros.uuid = uuid.uuid4()
            macros.command_answer = CommandAnswer(uuid=macros.uuid)
            for macros_command in macros.commands:
                macros_command.uuid = macros.uuid
                macros_command.command_answer = CommandAnswer(uuid=macros.uuid)
                # save_command_answer(macros_command)
                
        return item.uuid

    def add_command(self, item) -> uuid.UUID:
        """Добавить команду в очередь на выполнение"""
        uuid = self._assigns_uuid(item)
        if isinstance(item, Macros):
            logging.info(f"Add macros in pool: {item.uuid}")
            for command in item.commands:
                logging.info(f"Add macros command in pool: {command.uuid}")
                self._queue.put(command)
        else:
            logging.info(f"Add command in pool: {item.uuid}")
            self._queue.put(item)
        return uuid

    def start(self) -> None:
        """Запустить пул комманд"""
        self._thread.start()
