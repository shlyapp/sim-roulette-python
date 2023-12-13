from ...models.commands.command_callback import CommandCallback
from ...models.commands.types.command_status import CommandStatus
from ...database.tools import save_command_answer

from ...utils.logger import logger

class DefaultCommandCallback(CommandCallback):
    def callback(self, command) -> None:
        command_answer = command.command_answer
        if command_answer.status == CommandStatus.completed:
            logger.info(f"Command {command_answer.uuid} was finish success!")
        else:
            logger.error(f"Command {command_answer.uuid} was finish with error!")
        logger.info(f"Command answer: {command_answer.message}")
        save_command_answer(command)
