from enum import Enum


class CommandType(str, Enum):
    command = "command"
    atcommand = "atcommand"
