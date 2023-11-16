from typing import Union
from fastapi import FastAPI

from ..src.database.tools import load_simcard
from ..src.scripts.scripts import get_sms

app = FastAPI()

simcards = load_simcard()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/simcard/{phone}")
def get_phone_number(phone: str):
    for simcard in simcards:
        if simcard._phone_number == phone:
            return {"cell": {"track": simcard._cell.track, "number": simcard._cell.number}, "phone_number": simcard._phone_number}
    return {"msg": "not found"}


@app.get("/simcard/sms/{phone}")
def get_sms_by_number(phone: str):
    for simcard in simcards:
        if simcard._phone_number == phone:
            sms = get_sms(simcard)
            return {"message": sms}
    else:
        return {"msg": "not found"}