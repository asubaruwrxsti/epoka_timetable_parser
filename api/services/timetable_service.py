from utils import table_scraping_utils as tsu
from api.config import Config

def get_timetable_data(day: str):
    html_content = tsu.get_html_content(Config.TIMETABLE_URL)
    timetable = tsu.get_timetable_for_day(html_content, day.title())
    return {
        "day": day,
        "timetable": tsu.parse_timetable_course_html(timetable[0])
    }