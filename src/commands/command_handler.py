from threading import Thread
from time import sleep
from typing import cast

from .command import Command
from .command_status import CommandStatus

def command_handler(command):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def command_answer_listener():
                while True:
                    if command.is_finish():
                        func(command)
                        return
                    sleep(2)
            thread = Thread(target=command_answer_listener)
            thread.start()
        return wrapper
    return decorator