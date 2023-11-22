from enum import Enum


class CommandType(str, Enum):
    """Типы комманд"""
    command = "command"
    """Обычная команад"""
    atcommand = "atcommand"
    """AT команда с дополнительным ответом"""
