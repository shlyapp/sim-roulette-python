from .cell import Cell
from .commands.at_commands import get_command_view_sms


class SIMCard():
    def __init__(self, cell: Cell, phone_number: str):
        self._cell = cell
        self._phone_number = phone_number
        
    def get_sms(self, count: int = 1):
        command = get_command_view_sms(count)
        while True:
            message = command.execute()
            if message.split()[1] != "ERROR": 
                return message