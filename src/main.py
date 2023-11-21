import logging

from .models.command import command_executor_thread, queue, Command, ATCommand


logging.basicConfig(
    filename="sim-roulette-python/src/logs2.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def main():
    command_executor_thread.start()
    while True:
        command_text = input("Please, input command text: ")
        if command_text.startswith('AT'):
            command = ATCommand(command_text=command_text)
        else:
            command = Command(command_text=command_text)
        logging.info(f"Add command {command_text} in queue")
        queue.put(command)

    
if __name__ == "__main__":
    main()
