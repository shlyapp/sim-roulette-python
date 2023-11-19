from pydantic import BaseModel

from .task_status import TaskStatus


class TaskResponse(BaseModel):
    uuid: str
    status: TaskStatus
    result: str = ""
