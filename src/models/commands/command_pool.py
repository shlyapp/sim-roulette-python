import logging
import uuid
import requests
import urllib

from queue import Queue, Empty
from threading import Thread

from .command_answer import CommandAnswer, CommandStatus

from ...config import URL, TOKEN


class CommandPool():
    def __init__(self) -> None:
        self._thread = Thread(
            target=self._command_executor
        )
        self._queue = Queue()
    
    def _get_answer_response(self) -> str:
        data = {
            'data': f'{TOKEN}'
        }
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        response = requests.get(url=full_url).text
        return response
    
    def _get_command_answer(self, step):
        while True:     
            response = self._get_answer_response()
            if response == "0#!#0":
                continue
            data = response.replace('#', '').split('!')
            
            if int(data[0]) == (step - 1):
                return data
    
    def _command_executor(self) -> None:
        while True:
            try:
                command = self._queue.get()
                command.command_answer.status = CommandStatus.in_progress
                step = command.execute()
                answer_message = self._get_command_answer(step)
                command.command_answer.message = answer_message
                if command.validate_answer():
                    command.command_answer.status = CommandStatus.completed
                else:
                    command.command_answer.status = CommandStatus.failed
                command.invoke_callback()
                                
            except Empty:
                pass

    def _assigns_uuid(self, item) -> uuid.UUID:
        item.uuid = uuid.uuid4()
        item.command_answer = CommandAnswer(
            uuid=item.uuid
        )
        
        return item.uuid
            
    def add_command(self, item) -> uuid.UUID:
        uuid = self._assigns_uuid(item)
        self._queue.put(item)
        return uuid

    def start(self) -> None:
        self._thread.start()
