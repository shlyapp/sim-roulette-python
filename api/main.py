import uuid
import logging
from fastapi import FastAPI
from queue import Queue, Empty
from threading import Thread

from .models.task import Task
from .models.task_status import TaskStatus
from .models.task_response import TaskResponse

from ..src.database.tools import load_simcard
from ..src.models.simcard import SIMCard
from ..src.scripts.scripts import get_sms


app = FastAPI()
queue = Queue()
simcards = load_simcard()

tasks = list()

def consumer(queue):
    while True:
        try:
            func = queue.get()
        except Empty:
            continue
        else:
            result = func()
            
            for task in tasks:
                if task.uuid == result.uuid:
                    tasks.remove(task)
            
            tasks.append(result)
            

consumer_thread = Thread(
    target=consumer,
    args=(queue,),
    daemon=True
)


def get_message(simcard: SIMCard, task: Task) -> TaskResponse:
    logging.info(f"Start task {task.uuid}")
    task.status = TaskStatus.in_progress
    try:
        result = get_sms(simcard)
        response = TaskResponse(
            uuid=task.uuid,
            status=TaskStatus.completed,
            result=result
        )
        logging.info(f"Task {task.uuid} was comleted succecfully")
        return response
    except Exception:
        response = TaskResponse(
            uuid=task.uuid,
            status=TaskStatus.failed,
            result=Exception
        )
        logging.error(f"Task {task.uuid} was completed with error")
        logging.error(Exception)


def have_phone_number(phone_number: str):
    for simcard in simcards:
        if simcard._phone_number == phone_number:
            return simcard
    return None


@app.get("/api/phone/{phone_number}")
async def get_phone_info(phone_number: str):
    simcard = have_phone_number(phone_number)
    if simcard == None: 
        return {'msg': 'not found'}
    
    return {'phone_number': phone_number, 
            'cell': {
                'track': simcard._cell.track,
                'number': simcard._cell.number
            }}


@app.get("/api/result/{uuid_request}")
async def get_request_result(uuid_request: str):
    for task in tasks:
        if task.uuid == uuid_request:
            return task
    return {"msg": "not found"}


@app.post("/api/phone/{phone_number}/message")
async def add_task(phone_number: str):
    logging.info(f'Add new task to get message from {phone_number}')
    simcard = have_phone_number(phone_number)
    if simcard == None:
        return {'msg': 'not found phone number'}
    
    task = Task(
        uuid=str(uuid.uuid4()),
        status=TaskStatus.pending
    )
    logging.info(f'Task {task.uuid} has been add in queue')
    tasks.append(task)
    queue.put(lambda: get_message(simcard, task))
    return task




