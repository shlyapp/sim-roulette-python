from abc import ABC, abstractmethod

class CommandValidator(ABC):
    @abstractmethod
    def validate(self, response, *args) -> bool:
        pass