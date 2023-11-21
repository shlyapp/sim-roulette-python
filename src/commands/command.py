import logging
import requests
import urllib

from .command_type import CommandType
from ..config import TOKEN, STEP, URL


class Command:
    """Команда"""
    def __init__(self, command_text: str):
        self.command_text = command_text
        """Текст комманды"""
        self.type = CommandType.command
        """Тип команды"""
        self.uuid = None
        """UUID"""
        self.command_answer = None
        """Ответ на команду"""
        if command_text.startswith("AT"):
            self.type = CommandType.atcommand
        
    def execute(self):
        """Выполнение команды, отправка запроса на сервер"""
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
