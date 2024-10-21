from fastapi import FastAPI
from api.routes import timetable
from api.config import Config
import uvicorn
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

class API:
    def __init__(self, app: FastAPI = None):
        self.app = app or FastAPI()
        self.limiter = Limiter(key_func=get_remote_address)
        self.setup_middleware()
        self.setup_routes()

    def setup_middleware(self):
        self.app.state.limiter = self.limiter
        self.app.add_middleware(SlowAPIMiddleware)

    def setup_routes(self):
        self.app.include_router(timetable.router)

    def run(self):
        uvicorn.run("api.api:app", host=Config.API_HOST, port=Config.API_PORT, reload=Config.API_HOT_RELOAD)

api_instance = API()
app = api_instance.app