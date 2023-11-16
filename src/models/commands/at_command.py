import requests
import urllib

from time import sleep

from ...config import TOKEN, URL, STEP
from ...utils import parse_response

from .command import Command


class ATCommand(Command):
    def __init__(self, command_text: str):
        self._base_command_text = "modem>send:"
        super().__init__(self._base_command_text + command_text)
        
    def execute(self):
        global STEP
        while True:
            data = {
                'data': f'{TOKEN}||{STEP}||{self._command_text}'
            }
            encoded_data = urllib.parse.urlencode(data)
            full_url = f'{URL}?{encoded_data}'

            response = requests.get(url=full_url).text
            step, code = parse_response(response)
            if int(step) == STEP:
                response = requests.get(url=full_url).text
                STEP += 1
                return response
            sleep(5)