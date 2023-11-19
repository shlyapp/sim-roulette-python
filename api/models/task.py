from pydantic import BaseModel

from .task_status import TaskStatus


class Task(BaseModel):
    uuid: str
    status: TaskStatus
