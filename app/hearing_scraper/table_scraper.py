import requests
from bs4 import BeautifulSoup
import pandas as pd

def getData(url):
    base_url = url
    response = requests.get(base_url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table', class_='has-fixed-layout')
    table_rows = soup.find_all('tr')[1:]

    header = []
    header = soup.find_all('th')
    header = [h.text.strip() for h in header]

    data = []
    for row in table_rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    df = pd.DataFrame(data, columns=header)
    return df

# gets the  table data in pandas datframe from the url
# url = "https://www.cdcr.ca.gov/bph/2024/03/20/hearing-results-february-2024/"
# data = getData(url)
# print(data)