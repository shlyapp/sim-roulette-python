from ..models.commands.modem_commands import *
from ..models.commands.card_commands import *
from ..models.commands.buffer_commands import *
from ..models.commands.at_commands import *
from ..models.commands.sms_commands import *
from ..models.cell import Cell
from ..models.simcard import SIMCard

from ..utils import get_number_from_sms


def connect():
    """Присоединяет и включает модем"""
    modem_connect.execute()
    modem_on.execute()
    

def check_have_sim(cell: Cell):
    """Проверяет наличия СИМ-карты в ячейке"""
    command = get_command_select_card(cell)
    command.execute()
    have_simcard = card_discover.execute()
    if have_simcard:
        connect()
        phone = get_phone_buffer()
        sim = SIMCard(cell, phone)
        return sim

    return None


def get_phone_buffer():
    """Возвращает номер телефона из буфера"""
    buffer_fs_load_phone.execute()
    phone = buffer_view.execute()
    return phone


def get_real_phone(simcard: SIMCard):
    """Возвращает реальный номер телефона, полученный СМС ответом"""
    sms_clear.execute()
    command = get_command_call_code("*111*0887#")
    command.execute()
    # fix that, need 2 response to get answer
    simcard.get_sms()
    return get_number_from_sms(simcard.get_sms())


def update_number(phone_number):
    """Обновляет значение номера телефона в буфере"""
    buffer_clear.execute()
    command = get_command_buffer_write(phone_number)
    command.execute()
    buffer_fs_save_phone.execute()


def init():
    """Выводит информацию о СИМ-карте в ячейке"""
    for i in range(10):
        cell = Cell('A', i)
        sim = check_have_sim(cell)
        print(f'Ячейка: {cell.track}{cell.number}')
        if sim is not None:
            print('В ячейке есть СИМ-карта')
            print(f'Номер телефона: {sim._phone_number}')
            print(f'Реальный номер: {get_real_phone(sim)}')
        else:
            print('Нет СИМ-карты в ячейке')
            
    
    