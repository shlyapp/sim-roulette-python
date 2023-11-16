from pydantic import BaseModel

from .task_status import TaskStatus


class Task(BaseModel):
    id: int
    status: TaskStatus