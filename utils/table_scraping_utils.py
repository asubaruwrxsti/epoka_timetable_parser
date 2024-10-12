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
    for row in rows:
        pattern = re.compile(r'<(th|td)[^>]*>(.*?)</\1>', re.DOTALL)
        cells = pattern.findall(row)
        row_data = [cell[1].strip() for cell in cells]
        
        # Check if the first element is a string number
        if row_data and row_data[0].isdigit():
            row_data = row_data[1:]
        
        table_data.append(row_data)
    
    return table_data

def get_timetable_days(html_content):
    days = []

    table_headers = get_table_headers(html_content)
    day_index = table_headers.index("Day")

    rows = get_table_rows(html_content)
    for index, row in enumerate(rows):
        if index == 0:
            day = row[day_index]
        else:
            day = row[day_index - 1]
        if day not in days:
            days.append(day)
    
    return days

def get_timetable_times(html_content):
    table_headers = get_table_headers(html_content)
    return [header for header in table_headers if re.match(r'\d{2}:\d{2}- \d{2}:\d{2}', header)]

def get_timetable_for_day(html_content, day):
    table_rows = get_table_rows(html_content)
    return [row for row in table_rows if row[0] == day]

def parse_timetable_course_html(course_html):
    courses = []
    
    if isinstance(course_html, list):
        for course in course_html[1:]:
            if len(course) < 2: 
                continue
            
            soup = BeautifulSoup(course, 'lxml')
            
            tt_code_elements = soup.find_all(class_='tt-code')
            tt_full_name_elements = soup.find_all(class_='tt-full-name')
            tt_details_elements = soup.find_all(class_='tt-details')
            
            for tt_code, tt_full_name, tt_details in zip(tt_code_elements, tt_full_name_elements, tt_details_elements):
                if not tt_code or not tt_full_name or not tt_details:
                    continue
                
                course_code = tt_code.text.strip()
                course_name = tt_full_name.find('em').text.strip()
                classroom = tt_details.find('span').text.strip()
                
                courses.append({
                    'course_code': course_code,
                    'course_name': course_name,
                    'classroom': classroom
                })
    
    return courses

def get_html_content(url):
    response = requests.get(url)
    return response.text