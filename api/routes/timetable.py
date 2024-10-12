# api/routes/timetable.py
from fastapi import APIRouter
from api.services.timetable_service import get_timetable_data
import time

router = APIRouter()

@router.get("/timetable")
def get_timetable(day: str = time.strftime("%A")):
    return get_timetable_data(day)

@router.get("/timetable/{day}")
def get_timetable_for_day(day: str):
    return get_timetable_data(day)