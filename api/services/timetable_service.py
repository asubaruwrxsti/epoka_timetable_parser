from utils import table_scraping_utils as tsu
from api.config import Config

def get_timetable_data(day: str):
    try:
        html_content = tsu.get_html_content(Config.TIMETABLE_URL)
        timetable, column_span_map = tsu.get_timetable_for_day(html_content, day.title())
        return {
            "day": day.title(),
            "timetable": tsu.parse_timetable_course_html(timetable[0], column_span_map)
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "I suppose the day we are looking for is not in the timetable ? 🤔"
        }

def get_whole_timetable_data():
    timetable = {}

    html_content = tsu.get_html_content(Config.TIMETABLE_URL)
    all_days = tsu.get_timetable_days(html_content)

    print(all_days)

    for day in all_days:
        day_timetable = tsu.get_timetable_for_day(html_content, day)
        if isinstance(day_timetable, list) and len(day_timetable) > 0:
            timetable[day] = tsu.parse_timetable_course_html(day_timetable[0])
        else:
            timetable[day] = None

    return timetable