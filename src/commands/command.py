import requests
import urllib
import uuid

from .command_answer import CommandAnswer
from .command_type import CommandType
from .command_status import CommandStatus
from .command_handler import command_finish
from ..config import TOKEN, STEP, URL


class Command:
    """Команда"""
    def __init__(self, command_text: str):
        self.command_text = command_text
        """Текст комманды"""
        self.type = CommandType.command
        """Тип команды"""
        self.uuid = uuid.uuid4()
        """UUID"""
        self.command_answer = CommandAnswer(uuid=uuid.uuid4())
        """Ответ на команду"""
        self.finish_event()
        if command_text.startswith("AT"):
            self.type = CommandType.atcommand
    
    @command_finish()
    def finish_event(self) -> None:
        print("Command has been complete")
    
    def execute(self) -> int:
        """Выполнение команды, отправка запроса на сервер"""
        global STEP
        data = {
            'data': f'{TOKEN}||{STEP}||{self.command_text}'
        }
        
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        requests.get(url=full_url).text
        STEP = STEP + 1
        return STEP
    
    def is_finish(self) -> bool:
        if self.command_answer.status in [CommandStatus.failed, CommandStatus.completed]:
            return True
        return False
