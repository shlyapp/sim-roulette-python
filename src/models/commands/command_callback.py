from abc import ABC, abstractmethod

class CommandCallback(ABC):
    @abstractmethod
    def callback(self, command) -> bool:
        pass