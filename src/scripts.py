import logging

from .models.commands.modem_commands import *
from .models.commands.card_commands import *

from .models.cell import Cell
from .models.command import QUEUE_THREAD


def connect(cell: Cell) -> None:
    """Присоединяет и включает модем"""
    select_card = get_command_select_card(cell)
    QUEUE_THREAD.put(select_card)
    QUEUE_THREAD.put(modem_connect)
    QUEUE_THREAD.put(modem_on)
    QUEUE_THREAD.put(modem_activation)