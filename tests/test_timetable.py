from fastapi.testclient import TestClient
from api.api import app
from api.config import Config

client = TestClient(app)

def test_get_timetable_unauthorized():
    response = client.get("/timetable")
    assert response.status_code == 401

def test_get_timetable_authorized():
    response = client.get("/timetable", auth=(Config.API_USERNAME, Config.API_PASSWORD))
    assert response.status_code == 200
    assert "day" in response.json()
    assert "timetable" in response.json()

def test_get_whole_timetable_unauthorized():
    response = client.get("/timetable/week/")
    assert response.status_code == 401

def test_get_whole_timetable_authorized():
    response = client.get("/timetable/week/", auth=(Config.API_USERNAME, Config.API_PASSWORD))
    assert response.status_code == 200
    assert isinstance(response.json(), dict)