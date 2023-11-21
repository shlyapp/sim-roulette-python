import requests
import logging
import urllib
import uuid
from queue import Queue, Empty
from threading import Thread
from typing import NamedTuple, Optional, List
from enum import Enum

from ..config import TOKEN, URL, STEP


class CommandStatus(str, Enum):
    completed = "completed"
    failed = "failed"


class Command:
    def __init__(self, command_text: str):
        self.command_text = command_text
        self.uuid = ""
        
    def execute(self) -> str:
        global STEP
        data = {
            'data': f'{TOKEN}||{STEP}||{self.command_text}'
        }
        
        logging.info(f'Send request with data: {data}')
        
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        requests.get(url=full_url).text
        STEP += 1
        logging.info(f'Command {self.command_text} has been execute')
        

class ATCommand(Command):
    def __init__(self, command_text: str):
        super().__init__(command_text)
        
    def execute(self) -> str:
        return super().execute()


class CommandAnswer(NamedTuple):
    uuid: str    
    result: CommandStatus
    message: Optional[str]


class CommandAnswerLogs():
    def __init__(self) -> None:
        self._logs = list()
        
    def add(self, command_answer: CommandAnswer) -> None:
        self._logs.append(command_answer)
        
    def find(self, uuid: str) -> List[CommandAnswer]:
        command_answers = list()
        for command_answer in self._logs:
            if command_answer.uuid:
                command_answers.append(command_answers)
        
        return command_answers


LOGS = CommandAnswerLogs()


class Macros():
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        self.uuid = ""
        
    def run(self):
        logging.info("Macros run")
        self.uuid = uuid.uuid4()
        for command in self.commands:
            command = Command(command.command_text)
            command.uuid = self.uuid
            QUEUE_THREAD.put(command)

        

def get_answer_response() -> str:
    data = {
        'data': f'{TOKEN}'
    }
    encoded_data = urllib.parse.urlencode(data)
    full_url = f'{URL}?{encoded_data}'

    response = requests.get(url=full_url).text
    return response


def get_command_answer(command: Command):
    global STEP
    while True:
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.replace('#', '').split('!')
        
        if int(data[0]) == (STEP - 1):
            logging.info(f"Result of execute command: {data[1]}")
            if data[1] is None or data[1] == "Error" or data[1] == 'NULL' or data[1] == "UNKNOWN COMMAND":
                return CommandAnswer(
                    uuid=command.uuid,
                    result=CommandStatus.failed,
                    message=data[1]
                )
            return CommandAnswer(
                    uuid=command.uuid,
                    result=CommandStatus.completed,
                    message=data[1]
                )


def get_at_command_answer(command: ATCommand):
    global step
    while True:
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.split()
        logging.info(data)
        
        if data[0].find(command.command_text) != -1:
            # typically -2 - code
            return data[-2]


def command_executor(queue: Queue):
    while True:
        try:
            command = queue.get()
            logging.info(f"Start command: {command.command_text}")
            logging.info(f"uuid: {command.uuid}")
            command.execute()
        except Empty:
            logging.info("queue empty")
            continue
        else:
            logging.info("Wait result of execute command")
            command_answer = get_command_answer(command)
            
            if isinstance(command, ATCommand):
                message = get_at_command_answer(command)
                command_answer = CommandAnswer(
                    uuid=command.uuid,
                    result=command_answer.result,
                    message=message
                )
            
            LOGS.add(command_answer)
            
            if queue.qsize() == 0:
                print(LOGS._logs)
            
            logging.info(f"Result: {command_answer.result}")
            logging.info(f"Message: {command_answer.message}\n")


QUEUE_THREAD = Queue()

COMMAND_EXECUTOR_THREAD = Thread(
    target=command_executor,
    args=(QUEUE_THREAD,),
    daemon=True
)