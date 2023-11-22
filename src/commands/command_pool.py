import logging

from queue import Queue, Empty
from typing import cast
from threading import Thread
from typing import cast

from .macros import Macros
from .command import Command
from .command_answer import *

from ..database.tools import save_command_answer


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
                    for i, command in enumerate(macros.commands):
                        command.command_answer.status = CommandStatus.in_progress
                        run_command(command)
                        
                        if i == len(macros.commands) - 1:
                            command.command_answer.message += " complete"
                            save_command_answer(command)
                        
                        logging.info(f"""
                                     Command answer
                                     uuid: {command.command_answer.uuid}
                                     status: {command.command_answer.status}
                                     message: {command.command_answer.message}
                                     """)
                        
                else:
                    command = cast(Command, item)
                    command.command_answer.status = CommandStatus.in_progress
                    run_command(command)
                    logging.info(f"""
                                     Command answer
                                     uuid: {command.command_answer.uuid}
                                     status: {command.command_answer.status}
                                     message: {command.command_answer.message}
                                     """)
            except Empty:
                pass

    def _assigns_uuid(self, item) -> uuid.UUID:
        if isinstance(item, Command):
            command = cast(Command, item)
            command.uuid = uuid.uuid4()
            command.command_answer = CommandAnswer(uuid=item.uuid)
            logging.info(f"Add command in pool: {command.uuid}")
            save_command_answer(command)
        else:
            macros = cast(Macros, item)
            macros.uuid = uuid.uuid4()
            macros.command_answer = CommandAnswer(uuid=macros.uuid)
            logging.info(f"Add macros in pool: {macros.uuid}")
            for macros_command in macros.commands:
                macros_command.uuid = macros.uuid
                macros_command.command_answer = CommandAnswer(uuid=macros.uuid)
                
        return item.uuid

    def add_command(self, item) -> uuid.UUID:
        """Добавить команду в очередь на выполнение"""
        uuid = self._assigns_uuid(item)
        self._queue.put(item)
        return uuid

    def start(self) -> None:
        """Запустить пул комманд"""
        self._thread.start()
