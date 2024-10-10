import re, time

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
            rows.append(tbody[start:end])
    return rows

def get_timetable_days(html_content):
    days = []

    table_headers = get_table_headers(html_content)
    day_index = table_headers.index("Day")

    rows = get_table_rows(html_content)
    for row in rows:
        # print(row)
        pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
        print(pattern.findall(row))
    
    return days


