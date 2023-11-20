from .database.tools import load_simcard
from .scripts.scripts import get_sms, init

from .config import TOKEN, URL, STEP
import urllib
from time import sleep
import requests

def get_current_result():
    data = {
        'data': f'{TOKEN}'
    }
    encoded_data = urllib.parse.urlencode(data)
    full_url = f'{URL}?{encoded_data}'

    response = requests.get(url=full_url).text
    return response


def main():
    init()


if __name__ == "__main__":
    main()
