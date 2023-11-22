from threading import Thread
from time import sleep
from typing import cast


def macros_finish():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            def command_answer_listener():
                while True:
                    command = self.command
                    if command.is_finish():
                        func(self, *args, **kwargs)
                        return
                    sleep(2)
            thread = Thread(target=command_answer_listener)
            thread.start()
        return wrapper
    return decorator

def command_finish():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            def command_answer_listener():
                while True:
                    if self.is_finish():
                        func(self, *args, **kwargs)
                        return
                    sleep(2)
            thread = Thread(target=command_answer_listener)
            thread.start()
        return wrapper
    return decorator