from ..models.cell import Cell
from ..commands.macros import Macros
from ..commands.command import Command
from .commands.modem import *
from .commands.card import *


def get_macros_check_card(cell: Cell) -> Macros:
    """Возврашает макрос для проверки наличия СИМ-карты"""
    check_card_macros = Macros([
        get_command_select_card(cell),
        card_discover
    ])
    return check_card_macros


def get_macros_connect(cell: Cell) -> Macros:
    """Возваращает макрос для подключения к СИМ-карте"""
    connect_macros = Macros([
        get_command_select_card(cell),
        modem_connect,
        modem_on,
        modem_activation
    ])
    return connect_macros


def get_macros_number(cell: Cell) -> Macros:
    """Возваращает макрос для подключения к СИМ-карте"""
    connect_macros = Macros([
        get_command_select_card(cell),
        modem_connect,
        modem_on,
        modem_activation,
        Command('AT+CUSD=1,"*110#"'),
        Command('AT+CMGR=1')
    ])
    return connect_macros