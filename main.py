import csv
import requests
from bs4 import BeautifulSoup


def beautify_texts(text):
    if isinstance(text, int):
        return text

    words = text.split()
    new_text = ''

    for word in words:
        new_text += word + ' '

    return new_text


def get_csv_file(year: int, report_months: list, vega: bool):
    headers = [f'{month} {i}' for month in report_months for i in ['I', 'II', 'III']]
    headers.insert(0, 'Наименование ирригационных систем и точек водовыделов')

    if vega:
        folder_name = 'vega'
    else:
        folder_name = 'mezhvega'

    file = open(f'{folder_name}/data_{year}.csv', 'w')
    csv_file = csv.writer(file)
    csv_file.writerow(headers)

    return csv_file


def parse_page(url: str, year: int, report_months: list, vega: bool):
    if vega:
        if year >= 2000:
            current_url = url % (year, str(year)[-2:])
        else:
            current_url = url % (year, year)
    else:
        if year >= 2018:
            current_url = url % (year, str(year)[-2:])
        elif year >= 2011:
            current_url = url % (year, str(year)[-2:] + '-' + str(year + 1)[-2:])
        elif year >= 2009:
            current_url = url % (year, str(year + 1)[-2:])
        elif year >= 2000:
            current_url = url % (year, str(year)[-2:])
        else:
            current_url = url % (year, str(year) + '-' + str(year + 1))

    response = requests.get(current_url)
    html_response = response.content.decode('cp1251')

    soup = BeautifulSoup(html_response, 'html.parser')

    table = soup.find_all('tbody')[0]
    rows = table.find_all('tr')[2:]

    csv_file = get_csv_file(year, report_months, vega)

    for row in rows:
        row_data_set = row.find_all('td')
        row_data_list = [beautify_texts(cell.text) for cell in row_data_set]
        csv_file.writerow(row_data_list)


start_year = 1991
end_year = 2020
vega_url = 'http://www.cawater-info.net/karadarya/%s/veg%s.htm'
mezhvega_url = 'http://www.cawater-info.net/karadarya/%s/mveg%s.htm'

months = [
    ['апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь'],
    ['октябрь', 'ноябрь', 'декабрь', 'январь', 'февраль', 'март']
]

for i in range(1991, 2021):
    parse_page(vega_url, i, report_months=months[0], vega=True)

for i in range(1991, 2021):
    parse_page(mezhvega_url, i, report_months=months[1], vega=False)