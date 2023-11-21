from typing import List

from .database import Database
from ..config import DATABASE
from ..models.simcard import SIMCard
from ..models.cell import Cell
from ..commands.command_answer import CommandAnswer
from ..commands.command import Command

database = Database(
    host=DATABASE['HOST'], 
    user=DATABASE['USER'], 
    password=DATABASE['PASSWORD'], 
    db=DATABASE['NAME'], 
    port=DATABASE['PORT']
)


def save_simcard(simcard: SIMCard) -> None:
    """Добавление новой СИМ-карты в БД"""
    try:
        cursor = database.cursor
        cursor.execute(f'''INSERT INTO main_simroulette (cell, phone_number) VALUES ('{simcard._cell.track}{simcard._cell.number}', '{simcard._phone_number}');''')
        database.commit()
    except:
        pass


def get_simcards() -> List[SIMCard]:
    """Возвращает все СИМ-карты из БД"""
    data = database.select(
        table='main_simroulette',
        columns=['cell', 'phone_number'],
    )
    
    simcards = []
    for element in data:
        track = element[0][0]
        number = element[0][1:]
        simcards.append(SIMCard(
            cell=Cell(track, number),
            phone_number=element[1]
        ))
    
    return simcards


def save_command_answer(command: Command, command_answer: CommandAnswer) -> None:
    database.insert(
        table='main_simroulettelogs',
        columns=['operation_uuid', 'command_text', 'status', 'message'],
        values=[command_answer.uuid, command.command_text, command_answer.status, command_answer.message]
    )

    database.commit()
