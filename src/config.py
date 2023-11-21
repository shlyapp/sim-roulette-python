import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
"""Токен для доступа к серверу"""

STEP = 1
"""Шаг команды"""

URL = "http://192.168.3.181/port"
"""URL"""

DATABASE = {
    'NAME': os.getenv("DB_NAME"),
    'USER': os.getenv("USER_NAME"),
    'PASSWORD': os.getenv("PASSWORD"),
    'HOST': os.getenv("HOST"),
    'PORT': os.getenv("PORT"),
}
