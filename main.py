import requests
from utils import table_scraping_utils as tsu

def main():
    timetable_url = "https://eis.epoka.edu.al/publictimetable/144/show/programgrade/35/"

    # with open("timetable.html", "w") as file:
    #     file.write(get_html_content(timetable_url))

    with open("timetable.html", "r") as file:
        html_content = file.read()
        table = tsu.get_timetable_for_day(html_content, "Monday")
        print(tsu.parse_timetable_course_html(table[0]))

def get_html_content(url):
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    main()