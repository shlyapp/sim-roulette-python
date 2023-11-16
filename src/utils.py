def parse_response(response_text: str) -> tuple:
    """Возвращает шаг операции и реультат"""
    couples = response_text.replace("#", "").split("!")
    return (couples[0], couples[1])


def get_number_from_sms(sms_text: str) -> str:
    """Возвращает номер телефона из смс оператора"""
    couples = sms_text.split()
    return couples[-2]