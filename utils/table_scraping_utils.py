import re, requests
from bs4 import BeautifulSoup

def get_table(html_content):
    start = html_content.find("<table")
    end = html_content.find("</table>") + len("</table>")
    return html_content[start:end]

def get_table_headers(html_content):
    pattern = re.compile(r'<th[^>]*>(.*?)</th>', re.DOTALL)
    headers = pattern.findall(html_content)
    return [header.strip() for header in headers]

def get_table_rows(html_content):

    start = html_content.find("<tbody>")
    end = html_content.find("</tbody>") + len("</tbody>")
    tbody = html_content[start:end]
    
    rows = []
    start = 0
    while start != -1:
        start = tbody.find("<tr>", start)
        if start != -1:
            start += len("<tr>")
            end = tbody.find("</tr>", start)
            row_content = tbody[start:end]
            rows.append(row_content)

    table_data = []
    column_span_map = {}
    for row in rows:
        pattern = re.compile(r'<(th|td)[^>]*>(.*?)</\1>', re.DOTALL)
        cells = pattern.findall(row)
        row_data = [cell[1].strip() for cell in cells]

        colspan_pattern = re.compile(r'colspan="(\d+)"', re.DOTALL)
        colspan_cells = colspan_pattern.findall(row)
        column_span_map.update({index: int(span) for index, span in enumerate(colspan_cells)})

        # Check if the first element is a string number
        if row_data and row_data[0].isdigit(): row_data = row_data[1:]
        table_data.append(row_data)
    return table_data, column_span_map

def get_timetable_days(html_content):
    days = []

    table_headers = get_table_headers(html_content)
    day_index = table_headers.index("Day")

    rows, _ = get_table_rows(html_content)
    for _, row in enumerate(rows):
        day = row[day_index - 1]
        if day not in days: days.append(day)
    
    return days

def get_timetable_times(html_content):
    table_headers = get_table_headers(html_content)
    return [header for header in table_headers if re.match(r'\d{2}:\d{2}- \d{2}:\d{2}', header)]

def get_timetable_for_day(html_content, day):
    table_rows, column_span_map = get_table_rows(html_content)
    return [row for row in table_rows if row[0] == day], column_span_map


def parse_timetable_course_html(course_html, column_span_map):
    courses = []

    html_content = get_html_content_from_file('timetable.html')
    timetable_times = get_timetable_times(html_content)
    
    if isinstance(course_html, list):
        previous_end_index = 0
        
        for index, course in enumerate(course_html[1:]):
            if len(course) < 2: continue
            
            soup = BeautifulSoup(course, 'lxml')
            
            tt_code_elements = soup.find_all(class_='tt-code')
            tt_full_name_elements = soup.find_all(class_='tt-full-name')
            tt_details_elements = soup.find_all(class_='tt-details')
            
            for tt_code, tt_full_name, tt_details in zip(tt_code_elements, tt_full_name_elements, tt_details_elements):
                if not tt_code or not tt_full_name or not tt_details: continue
                
                course_code = tt_code.text.strip()
                course_name = tt_full_name.find('em').text.strip() if tt_full_name.find('em') else ''
                classroom = tt_details.find('span').text.strip() if tt_details.find('span') else ''

                time_start_index = previous_end_index if previous_end_index else index
                time_start = timetable_times[time_start_index]
                span = column_span_map.get(index, 1)
                time_end_index = time_start_index + span
                time_end = timetable_times[time_end_index]

                courses.append({
                    'course_code': course_code,
                    'course_name': course_name,
                    'classroom': classroom,
                    'time_start': time_start,
                    'time_end': time_end
                })
                previous_end_index = time_end_index + 1

    return courses

def get_html_content(url):
    response = requests.get(url)
    with open('timetable.html', 'w') as file:
        file.write(response.text)
    return response.text

def get_html_content_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()