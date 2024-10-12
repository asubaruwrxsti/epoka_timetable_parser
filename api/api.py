# api/api.py
from fastapi import FastAPI
from api.routes import timetable
from api.config import Config
import uvicorn

class API:
    def __init__(self, app: FastAPI = None):
        self.app = app or FastAPI()
        self.setup_routes()

    def setup_routes(self):
        self.app.include_router(timetable.router)

    def run(self):
        uvicorn.run("api.api:app", host=Config.API_HOST, port=Config.API_PORT, reload=Config.API_HOT_RELOAD)

api_instance = API()
app = api_instance.app