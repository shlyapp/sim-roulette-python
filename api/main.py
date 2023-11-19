from fastapi import FastAPI
from queue import Queue, Empty
from threading import Thread
import uuid
from time import sleep

from .models.task import Task
from .models.task_status import TaskStatus
from .models.task_response import TaskResponse


app = FastAPI()
counter = 0
queue = Queue()

tasks = list()

def consumer(queue):
    while True:
        try:
            func = queue.get()
        except Empty:
            continue
        else:
            result = func()
            tasks.append(result)
            print(f"Задача {result.uuid} выполнена")
            

consumer_thread = Thread(
    target=consumer,
    args=(queue,),
    daemon=True
)


def get_message(phone_number: str, task: Task) -> TaskResponse:
    task.status = TaskStatus.in_progress
    print(f"Выполнение задачи: {task.uuid}")
    sleep(20)
    response = TaskResponse(
        uuid=task.uuid,
        status=TaskStatus.completed,
        result="Смс код: 1234"
    )
    return response


@app.get("/api/phone/{phone_number}")
async def get_phone_info(phone_number: str):
    pass


@app.get("/api/result/{uuid_request}")
async def get_request_result(uuid_request: str):
    for task in tasks:
        if task.uuid == uuid_request:
            return task
    for element in queue.queue:
        print(element.uuid)
        if element.uuid == uuid_request:
            return element


@app.post("/api/phone/{phone_number}/message")
async def add_task(phone_number: str):
    task = Task(
        uuid=str(uuid.uuid4()),
        status=TaskStatus.pending
    )
    print(f"Добавлена задача {task.uuid}")
    queue.put(lambda: get_message(phone_number, task))
    return task




