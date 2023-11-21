from ..command import Command


answer_on = Command("answer=1")
"""Разрешение вывода ответов команд в выходной поток"""

answer_off = Command("answer=0")
"""Запрещение вывода ответов команд в выходной поток"""

debug_on = Command("debug=1")
"""Разрешение вывода отладочной информации"""

debug_off = Command("debug=0")
"""Запрещение вывода отладочной инфмормации"""

answer_clear = Command("answer>clear")
"""Очистка буффера ответов"""

version = Command("version")
"""Текущая версия ПО"""

restart = Command("restart")
"""Soft-reset устройства"""