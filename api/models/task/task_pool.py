import concurrent.futures
from time import sleep

from .task_status import TaskStatus
from .task import Task


def any_task(task):
    print(f"Выполнение задачи {task.id}")
    sleep(15)
    print(f"Задача {task.id} выполнена")

class TaskPool:
    def __init__(self):
        self.tasks = []
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def execute_task(self, task):
        task.status = TaskStatus.in_progress
        any_task(task)
        task.status = TaskStatus.completed

    def add_task(self, task):
        self.tasks.append(task)
        self.executor.submit(self.execute_next_task)

    def execute_next_task(self):
        if self.tasks:
            next_task = self.tasks[-1]
            self.execute_task(next_task)
            # self.tasks.pop(0)