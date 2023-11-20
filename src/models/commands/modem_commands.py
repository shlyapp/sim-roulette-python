from enum import Enum

from .command import Command


class Mode(Enum):
    """Режимы работы модема"""
    TXT = "txt"
    PDU = "pdu"


def get_command_modem_set_step(steps: int) -> Command:
    """Возвращает команду для установки количества шагов привода контактной группы"""
    return Command(f"modem>set:step={steps}")


def get_command_modem_set_rate(rate: int) -> Command:
    """Возвращает скорость обмена данных с модемом"""
    return Command(f"modem>set:state={rate}")


def get_command_modem_set_mode(mode: Mode) -> Command:
    """Возвращает режим работы модема"""
    return Command(f"modem>set:state={mode}")


modem_connect = Command("modem>connect")
"""Подключение контактов к текущей СИМ-карте"""

modem_disconnect = Command("modem>disconnect")
"""Отключние контактов от СИМ-карты"""

modem_on = Command("modem>on")
"""Включение модема"""

modem_off = Command("modem>off")
"""Выключение модема"""

modem_activation = Command("modem>activation:bool")
"""Активация сети"""

modem_status_power = Command("modem>status:power")
"""Получение статуса питания модема"""

modem_status_connection = Command("modem>status:connect")
"""Получение статуса подключения контактов модема"""

modem_get_step = Command("modem>set:step")
"""Получение количество шагов привода контактной группы"""

modem_get_rate = Command("modem>set:rate")
"""Получение скорости порат для обмена данных с модемом"""

modem_get_mode = Command("modem>set:mode")
"""Получение режима работы модема"""