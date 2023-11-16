from .command import Command


def get_command_buffer_write(text: str) -> Command:
    """Возвращает команду для ввода новых данных в буффер"""
    return Command(f"buffer>write={text}")

buffer_clear = Command("buffer>command")
"""Очистка буфера"""

buffer_view = Command("buffer>view")
"""Вывод содержимого буфера"""

buffer_fs_load_phone = Command("buffer>fs>load>phone")
"""Чтение параметра 'Номер телефона'"""

buffer_fs_save_phone = Command("buffer>fs>save>phone")
"""Запись параметра 'Номер телефона'"""