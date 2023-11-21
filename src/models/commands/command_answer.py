import uuid
import requests
import urllib
import logging

from ...config import TOKEN, URL, STEP
from .command_status import CommandStatus
from .command import Command
from .at_command import ATCommand


class CommandAnswer():
    def __init__(self, uuid: uuid.UUID) -> None:
        self.uuid = uuid
        self.status = CommandStatus.pending
        self.message = ""


def get_answer_response() -> str:
    data = {
        'data': f'{TOKEN}'
    }
    encoded_data = urllib.parse.urlencode(data)
    full_url = f'{URL}?{encoded_data}'

    response = requests.get(url=full_url).text
    return response


def fill_command_answer(command: Command):
    global STEP
    while True:
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.replace('#', '').split('!')
        
        if int(data[0]) == (STEP - 1):
            logging.info(f"Result of execute command: {data[1]}")
            if data[1] is None or data[1] == "Error" or data[1] == 'NULL' or data[1] == "UNKNOWN COMMAND":
                command.command_answer.message = data[1]
                command.command_answer.status = CommandStatus.failed
                return

            command.command_answer.message = data[1]
            command.command_answer.status = CommandStatus.completed


def fill_at_command_answer(command: ATCommand):
    while True:
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.split()
        logging.info(data)
        
        if data[0].find(command.command_text) != -1:
            command.command_answer.message = data[-2]


def run_command(command: Command):
    logging.info(f"Start command: {command.command_text}")
    logging.info(f"uuid: {command.uuid}")
    command.execute()
    command.command_answer.status = CommandStatus.in_progress
    logging.info("Wait result of execute command")
    fill_command_answer(command)
    
    if isinstance(command, ATCommand):
        fill_at_command_answer(command)

