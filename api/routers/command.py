from fastapi import APIRouter

from ...src.database.tools import get_command_answer


command_router = APIRouter(
    prefix="/command",
    tags=["command"]
)


@command_router.get('/{uuid}')
def get_command_status(uuid: str):
    return get_command_answer(uuid)