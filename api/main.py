from typing import Union
from fastapi import FastAPI, HTTPException
import concurrent.futures

from ..src.database.tools import load_simcard
from ..src.scripts.scripts import get_sms

from .models.task.task import Task
from .models.task.task_response import TaskResponse
from .models.task.task_status import TaskStatus
from .models.task.task_pool import TaskPool

app = FastAPI()
task_pool = TaskPool()
executor = concurrent.futures.ThreadPoolExecutor()


@app.post("/submit_task/", response_model=Task)
async def submit_task():
    new_task = Task(id=len(task_pool.tasks) + 1, status=TaskStatus.pending)
    task_pool.add_task(new_task)
    return new_task


@app.get("/task_status/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: int):
    if task_id < 1 or task_id > len(task_pool.tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    task = task_pool.tasks[task_id - 1]
    if task.status == TaskStatus.completed:
        return TaskResponse(id=task.id, status=task.status, result=f"Task {task.id} completed")
    else:
        return TaskResponse(id=task.id, status=task.status)
# simcards = load_simcard()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/simcard/{phone}")
# def get_phone_number(phone: str):
#     for simcard in simcards:
#         if simcard._phone_number == phone:
#             return {"cell": {"track": simcard._cell.track, "number": simcard._cell.number}, "phone_number": simcard._phone_number}
#     return {"msg": "not found"}


# @app.get("/simcard/sms/{phone}")
# def get_sms_by_number(phone: str):
#     for simcard in simcards:
#         if simcard._phone_number == phone:
#             sms = get_sms(simcard)
#             return {"message": sms}
#     else:
#         return {"msg": "not found"}