import requests
import csv
import time

from bs4 import BeautifulSoup as bs

base_url = 'https://en.tutiempo.net/climate/'

cities = {
    "ws-421810": "New Delhi"
}

months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]

for city in cities:
    timestamp = time.strftime("%Y%m%d-%H%M")
    filename = f'{timestamp}-{cities[city]}.csv'
    csv_writer = csv.writer(open(filename, 'w'))

    csv_header_insert = False

    for year in years:
        for month in months:
            url_string = f'{base_url}{month}-{year}/{city}.html'
            url = requests.get(url_string)
            soup = bs(url.content, "html.parser")

            for table_row in soup.find(class_="mt5 minoverflow tablancpy").find_all('tr'):
                table_data = []

                for table_header in table_row.find_all('th'):
                    table_data.append(table_header.text)

                if table_data == ["Monthly means and totals:"]:
                    break

                if table_data:
                    if not csv_header_insert:
                        table_data = ["City", "Year", "Month"] + table_data
                        print("Inserting table headers: {}".format(','.join(table_data)))
                        csv_writer.writerow(table_data)
                        csv_header_insert = True
                    continue

                for table_row_data in table_row.find_all('td'):
                    table_data.append(table_row_data.text.strip())

                if table_data:
                    table_data = [cities[city], year, month] + table_data
                    print("Inserting table row data: {}".format(','.join(table_data)))
                    csv_writer.writerow(table_data)
                    continue
