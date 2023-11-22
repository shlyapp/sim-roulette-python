from ...commands.command import Command
from ...models.cell import Cell


def get_command_select_card(cell: Cell) -> Command:
    """Возвращает команду для выбора СИМ-карты"""
    return Command(f'card:{cell.track}{cell.number}')


def get_command_card_out(cell: Cell) -> Command:
    """Возвращает команду для подведения СИМ-карты для извлечения"""
    return Command(f'card>out:{cell.track}{cell.number}')


card_next = Command("card>next")
"""Выбор следующей СИМ-карты"""

card_prev = Command("card>prev")
"""Выбор предыдущей СИМ-карты"""

card_now = Command("card>now")
"""Полученеие номера выбранной в данной момент СИМ-карты"""

card_discover = Command("card>discover")
"""Проверка наличия СИМ-карты в текущей ячейке"""

card_begin = Command("card>begin")
"""Отметка текущей СИМ-карты как первой в последующем цикле действий"""
