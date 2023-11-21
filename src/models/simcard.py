from .cell import Cell


class SIMCard():
    """СИМ-карта"""
    def __init__(self, cell: Cell, phone_number: str):
        self.cell = cell
        """Ячейка"""
        self.phone_number = phone_number
        """Номер телефона"""
