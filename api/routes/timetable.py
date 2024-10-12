from fastapi import APIRouter
from api.services.timetable_service import get_timetable_data, get_whole_timetable_data
import time

router = APIRouter()

@router.get("/timetable")
def get_timetable(day: str = None):
    if day is None: day = time.strftime("%A")
    return get_timetable_data(day)

@router.get("/timetable/week/")
def get_whole_timetable():
    return get_whole_timetable_data()