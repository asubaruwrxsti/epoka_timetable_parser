import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TIMETABLE_URL = os.getenv("TIMETABLE_URL")
    API_HOST = os.getenv("API_HOST")
    API_PORT = int(os.getenv("API_PORT"))
    API_HOT_RELOAD = os.getenv("API_HOT_RELOAD") == "True"