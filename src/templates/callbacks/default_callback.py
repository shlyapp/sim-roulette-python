from ...models.commands.command_callback import CommandCallback
from ...models.commands.types.command_status import CommandStatus
from ...database.tools import save_command_answer

class DefaultCommandCallback(CommandCallback):
    def callback(self, command) -> None:
        command_answer = command.command_answer
        if command_answer.status == CommandStatus.completed:
            print(f"Command {command_answer.uuid} was finish success!")
        else:
            print(f"Command {command_answer.uuid} was finish with error!")
        save_command_answer(command)
