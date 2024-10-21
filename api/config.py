import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TIMETABLE_URL = os.getenv("TIMETABLE_URL")
    API_HOST = os.getenv("API_HOST")
    API_PORT = int(os.getenv("API_PORT"))
    API_HOT_RELOAD = os.getenv("API_HOT_RELOAD") == "True"
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")
    API_RATE_LIMIT = os.getenv("API_RATE_LIMIT")