from typing import List
import uuid

from .database import Database
from ..config import DATABASE
from ..models.simcard import SIMCard
from ..models.cell import Cell

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


def save_command_answer(command) -> None:
    database.insert_or_update(
        table='main_simroulettelogs',
        columns=['operation_uuid', 'command_text', 'status', 'message'],
        values=[(str(command.command_answer.uuid), 
                command.command_text, 
                command.command_answer.status.value, 
                command.command_answer.message)],
        unique_columns=['operation_uuid', 'command_text']
    )
    
from ..models.commands.command_answer import CommandAnswer

def get_command_answer(uuid: uuid.UUID):
    print(uuid)
    data = database.select(
        table='main_simroulettelogs',
        columns=['operation_uuid', 'status', 'message'],
        condition={'operation_uuid': str(uuid)}
    )
    
    commands_answers = list()
    for element in data:
        answer = CommandAnswer(uuid=element[0])
        answer.status = element[1]
        answer.message = element[2]
        commands_answers.append(answer)
    
    return commands_answers