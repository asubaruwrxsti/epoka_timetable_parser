from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from api.services.timetable_service import get_timetable_data, get_whole_timetable_data
import time
from api.config import Config
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
security = HTTPBasic()

limiter = Limiter(key_func=get_remote_address)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = Config.API_USERNAME
    correct_password = Config.API_PASSWORD
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.get("/timetable")
@limiter.limit(Config.API_RATE_LIMIT)
def get_timetable(request: Request, day: str = None, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    if day is None: day = time.strftime("%A")
    return get_timetable_data(day)

@router.get("/timetable/week/")
@limiter.limit(Config.API_RATE_LIMIT)
def get_whole_timetable(request: Request, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_whole_timetable_data()