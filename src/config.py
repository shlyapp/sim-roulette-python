import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

STEP = 1
URL = "http://192.168.3.181/port"

DATABASE = {
    'NAME': os.getenv("DB_NAME"),
    'USER': os.getenv("USER_NAME"),
    'PASSWORD': os.getenv("PASSWORD"),
    'HOST': os.getenv("HOST"),
    'PORT': os.getenv("PORT"),
}