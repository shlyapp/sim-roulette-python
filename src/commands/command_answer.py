import uuid
import requests
import urllib
import logging

from ..config import TOKEN, URL
from .command_status import CommandStatus
from .command_type import CommandType
from ..database.tools import save_command_answer


class CommandAnswer():
    """Ответ на выполнение команды"""
    def __init__(self, uuid: uuid.UUID) -> None:
        self.uuid = uuid
        """UUID"""
        self.status = CommandStatus.pending
        """Статус выполнения"""
        self.message = ""
        """Ответ на команду"""


def get_answer_response() -> str:
    """Возвращает ответ на команду"""
    data = {
        'data': f'{TOKEN}'
    }
    encoded_data = urllib.parse.urlencode(data)
    full_url = f'{URL}?{encoded_data}'

    response = requests.get(url=full_url).text
    return response


def fill_command_answer(command, step) -> None:
    """Заполняет данные ответа у команды"""
    while True:     
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.replace('#', '').split('!')

        if int(data[0]) == (step - 1):
            if data[1] is None or data[1] == "Error" or data[1] == 'NULL' or data[1] == "UNKNOWN COMMAND":
                command.command_answer.message = data[1]
                command.command_answer.status = CommandStatus.failed
                save_command_answer(command)
                return

            command.command_answer.message = data[1]
            command.command_answer.status = CommandStatus.completed
            save_command_answer(command)
            return


def fill_at_command_answer(command) -> None:
    """Заполняет дополнительные поля у at command"""
    while True:
        response = get_answer_response()
        if response == "0#!#0":
            continue
        data = response.split()
        
        if data[0].find(command.command_text) != -1:
            command.command_answer.message = data[-2]


def run_command(command) -> None:
    """Запускает выполнение команды и получает ответ"""
    logging.info(f"""
                 Execute command
                 uuid: {command.uuid}
                 command_text: {command.command_text}
                 """)
    step = command.execute()
    save_command_answer(command)
    command.command_answer.status = CommandStatus.in_progress
    fill_command_answer(command, step)
    
    if command.type == CommandType.atcommand:
        fill_at_command_answer(command)
