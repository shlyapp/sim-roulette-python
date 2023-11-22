from fastapi import APIRouter

from ...src.database.tools import get_simcards
from ...src.tools.macros import get_macros_message
from ...src.commands.command_pool import CommandPool

phone_router = APIRouter(
    prefix="/phone",
    tags=["phone"]
)

command_pool = CommandPool()
command_pool.start()

@phone_router.get('/')
def get_all_phone_numbers():
    simcards = get_simcards()
    return simcards

@phone_router.get('/{phone_number}')
def get_phone_number_info(phone_number: str):
    simcards = get_simcards()
    for simcard in simcards:
        if simcard.phone_number == phone_number:
            return simcard
    return {'msg': 'not found'}


@phone_router.post('/{phone_number}/message')
def get_message(phone_number: str):
    simcards = get_simcards()
    for simcard in simcards:
        if simcard.phone_number == phone_number:
            macros = get_macros_message(simcard.cell)
            uuid = command_pool.add_command(macros)
            return {'uuid_operation': uuid}
    return {'msg': 'not found'}
            