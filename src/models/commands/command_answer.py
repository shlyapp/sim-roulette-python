import uuid

from .types.command_status import CommandStatus


class CommandAnswer():
    def __init__(self, uuid: uuid.UUID) -> None:
        self.uuid = uuid
        self.status = CommandStatus.pending
        self.message = ""
        
    def __str__(self):
        return f"UUID: {self.uuid}\nSTATUS: {self.status}\nMESSAGE: {self.message}"
