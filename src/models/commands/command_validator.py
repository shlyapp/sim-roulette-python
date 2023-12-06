from abc import ABC, abstractmethod

class CommandValidator(ABC):
    @abstractmethod
    def validate(self, command) -> bool:
        if command.command_answer.message == "":
            return False