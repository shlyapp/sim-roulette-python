from fastapi import FastAPI

from .routers.phone import phone_router 
from .routers.command import command_router
from .routers.service import service_router


app = FastAPI()
app.include_router(phone_router)
app.include_router(command_router)
app.include_router(service_router)


@app.get('/')
def get_welcome():
    return {'hello', 'world'}




