from ..command import Command


def get_command_sms_send(phone: str, message: str) -> Command:
    """Отправка SMS"""
    return Command(f"sms>send:{phone};{message}")


sms_discover = Command("sms>discover")
"""Проверка наличия SMS на СИМ-карте"""

sms_read = Command("sms>read")
"""Копирования одного SMS в буффер"""

sms_send_buffer = Command("sms>send>buffer")
"""Отправка SMS из буфера"""

sms_clear = Command("sms>clear")
"""Удаление всех SMS с СИМ-карты"""
