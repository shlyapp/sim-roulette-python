import logging
import requests
import urllib

from ...config import TOKEN, STEP, URL


class Command:
    def __init__(self, command_text: str):
        self.command_text = command_text
        self.uuid = None
        self.command_answer = None
        
    def execute(self):
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
