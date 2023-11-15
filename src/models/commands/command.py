import requests
import urllib

from time import sleep

from ...config import TOKEN, URL, STEP
from ...utils import parse_response

class Command():
    def __init__(self, command_text: str):
        self._command_text = command_text

    def execute(self):
        global STEP
        while True:
            data = {
                'data': f'{TOKEN}||{STEP}||{self._command_text}'
            }
            encoded_data = urllib.parse.urlenvcode(data)
            full_url = f'{URL}?{encoded_data}'

            response = requests.get(url=full_url).text
            step, code = parse_response(response)
            if int(step) == STEP:
                STEP += 1
                if code == 'NULL':
                    return None
                return code

            sleep(2)
             

