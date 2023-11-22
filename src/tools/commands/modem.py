from ...commands.command import Command


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
