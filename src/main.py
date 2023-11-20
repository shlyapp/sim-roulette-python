from .database.tools import load_simcard
from .scripts.scripts import get_sms, init

from .config import TOKEN, URL, STEP
import urllib
from time import sleep
import requests
from threading import Thread
import logging
from typing import NamedTuple, Optional
from queue import Queue, Empty
from enum import Enum


logging.basicConfig(
    filename="sim-roulette-python/src/logs2.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

step = 1
queue = Queue()

class CommandStatus(str, Enum):
    completed = "completed"
    failed = "failed"


class CommandAnswer(NamedTuple):
    command_text: str    
    result: CommandStatus
    message: Optional[str]


class Command:
    def __init__(self, command_text: str):
        self.command_text = command_text
        
    def execute(self) -> str:
        global step
        data = {
            'data': f'{TOKEN}||{step}||{self.command_text}'
        }
        
        logging.info(f'Send request with data: {data}')
        
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        requests.get(url=full_url).text
        step += 1
        logging.info(f'Command {self.command_text} has been execute')


class ATCommand(Command):
    def __init__(self, command_text: str):
        super().__init__(command_text)
        
    def execute(self) -> str:
        return super().execute()


def command_executor(queue: Queue):
    while True:
        try:
            command = queue.get()
            logging.info(f"Start command: {command.command_text}")
            command.execute()
        except Empty:
            continue
        else:
            logging.info("Wait result of execute command")
            
            command_answer = get_command_answer(command)
            
            if isinstance(command, ATCommand):
                message = get_command_answer_data(command)
                command_answer = CommandAnswer(
                    command_text=command.command_text,
                    result=command_answer.result,
                    message=message
                )
            
            logging.info(f"Result: {command_answer.result}")
            logging.info(f"Message: {command_answer.message}\n")


def get_command_answer(command: Command):
    global step
    while True:
        data = {
            'data': f'{TOKEN}'
        }
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        response = requests.get(url=full_url).text
        if response == "0#!#0":
            continue
        data = response.replace('#', '').split('!')
        
        if int(data[0]) == (step - 1):
            logging.info(f"Result of execute command: {data[1]}")
            if data[1] is None or data[1] == "Error" or data[1] == 'NULL' or data[1] == "UNKNOWN COMMAND":
                return CommandAnswer(
                    command_text=command.command_text,
                    result=CommandStatus.failed,
                    message=data[1]
                )
            return CommandAnswer(
                    command_text=command.command_text,
                    result=CommandStatus.completed,
                    message=data[1]
                )


def get_command_answer_data(command: Command):
    global step
    while True:
        data = {
            'data': f'{TOKEN}'
        }
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        response = requests.get(url=full_url).text
        if response == "0#!#0":
            continue
        data = response.split()
        logging.info(data)
        
        if data[0].find(command.command_text) != -1:
            # typically -2 - code
            return data[-2]
        
        
command_executor_thread = Thread(
    target=command_executor,
    args=(queue,),
    daemon=True
)


def main():
    command_executor_thread.start()
    while True:
        command_text = input("Please, input command text: ")
        if command_text.startswith('AT'):
            command = ATCommand(command_text=command_text)
        else:
            command = Command(command_text=command_text)
        logging.info(f"Add command {command_text} in queue")
        queue.put(command)

    
if __name__ == "__main__":
    main()
