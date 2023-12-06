import requests
import urllib
import uuid

from .command_validator import CommandValidator
from .command_callback import CommandCallback
from .types.command_type import CommandType
from .command_answer import CommandAnswer
from ...config import TOKEN, STEP, URL

from ...templates.callbacks.callbacks import default_command_callback
from ...templates.validators.validators import default_command_validator

class Command:
    def __init__(self,
                 command_text: str, 
                 callback: CommandCallback = default_command_callback, 
                 validator: CommandValidator = default_command_validator):
        self.command_text = command_text
        self.type = CommandType.command
        self.uuid = uuid.uuid4()
        self.command_answer = CommandAnswer(uuid=uuid.uuid4())
        self.callback = callback
        self.validator = validator
        if command_text.startswith("AT"):
            self.type = CommandType.atcommand
        
    def execute(self) -> int:
        global STEP
        data = {
            'data': f'{TOKEN}||{STEP}||{self.command_text}'
        }
        
        encoded_data = urllib.parse.urlencode(data)
        full_url = f'{URL}?{encoded_data}'

        requests.get(url=full_url).text
        STEP = STEP + 1
        return STEP
    
    def validate_answer(self) -> bool:
        return self.validator.validate(self)

    def invoke_callback(self):
        if hasattr(self, 'callback'):
            self.callback.callback(self)
            