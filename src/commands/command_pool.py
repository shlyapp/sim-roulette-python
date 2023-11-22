import logging

from queue import Queue, Empty
from typing import cast
from threading import Thread

from .macros import Macros
from .command import Command
from .command_answer import *


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
                
                if isinstance(item, Macros):
                    macros = cast(Macros, item)
                    for command in macros.commands:
                        command.command_answer.status = CommandStatus.in_progress
                        run_command(command)
                        logging.info(f"""
                                     Command answer
                                     uuid: {command.command_answer.uuid}
                                     status: {command.command_answer.status}
                                     message: {command.command_answer.status}
                                     """)
                else:
                    command = cast(Command, item)
                    command.command_answer.status = CommandStatus.in_progress
                    run_command(command)
                    logging.info(f"""
                                     Command answer
                                     uuid: {command.command_answer.uuid}
                                     status: {command.command_answer.status}
                                     message: {command.command_answer.status}
                                     """)
            except Empty:
                pass

    def add_command(self, item) -> uuid.UUID:
        """Добавить команду в очередь на выполнение"""
        item.uuid = uuid.uuid4()
        item.command_answer = CommandAnswer(uuid=item.uuid)
        logging.info(f"Add command in pool: {item.uuid}")
        self._queue.put(item)
        return item.uuid

    def start(self) -> None:
        """Запустить пул комманд"""
        self._thread.start()
