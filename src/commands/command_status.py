from enum import Enum


class CommandStatus(str, Enum):
    """Статусы выполнения комманд"""
    pending = "pending"
    """Ожидает на выполнение"""
    in_progress = "in_progress"
    """В процессе выполнения"""
    completed = "completed"
    """Успешно выполнена"""
    failed = "failed"
    """Выполнена с ошибкой"""