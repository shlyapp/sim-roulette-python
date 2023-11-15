def parse_response(response_text: str) -> tuple:
    couples = response_text.replace("#", "").split("!")
    return (couples[0], couples[1])
