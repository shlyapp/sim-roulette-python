from pydantic import BaseModel

from .task_status import TaskStatus


class TaskResponse(BaseModel):
    id: int
    status: TaskStatus
    result: str = ""