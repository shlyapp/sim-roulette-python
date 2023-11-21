from .command import Command


class ATCommand(Command):
    def __init__(self, command_text: str):
        super().__init__(command_text)


    def execute(self):
        return super().execute()
