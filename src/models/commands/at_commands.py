from .at_command import ATCommand
from .command import Command


def get_command_view_sms(count: int = 1):
    """Возвращает команду для чтения SMS"""
    return ATCommand(f"AT+CMGR={count}")


def get_command_call_code(code: str):
    """Возвращает команду для выполнения запроса"""
    return Command(f"ATD{code}")


def get_command_call_phone(phone: str):
    """Возвращает команду для звонка на телефон"""
    return ATCommand(f"ATD+{phone}")