import yaml
from .html_parser import *
from enum import Enum
from urllib.request import urlopen
from ssl import SSLError, CertificateError
from urllib.error import HTTPError, URLError
import requests
import pandas as pd
from bs4 import BeautifulSoup

property_file_path = "scrapper.yaml"
month_h3_id_property_key = "h3_id_month"
month_h3_string_property_key = "h3_string_month"
week_h3_id_property_key = "h3_id_week"


class URLType(Enum):
    HEARING_SCHEDULE = "hearing-schedules"
    HEARING_RESULTS = "hearing-results"


class SR_SCRAPER:

    def getData(self, base_url):
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

    def get_property_value(self, type: URLType, key: str):
        # Read the config file and return the value for key
        try:
            with open(property_file_path, "r") as file:
                config = yaml.safe_load(file)
        except Exception as e:
            print("Error while reading config file: " + str(e))
            raise e
        try:
            return config[type.value][key]
        except Exception as e:
            print("Error fetching key value: " + str(e))
            raise e

    def get_property(self, domain, property_name):
        return self.get_property_value(domain, property_name)

    def get_hearing_schedule_base_url(self):
        return self.get_property_value(URLType.HEARING_SCHEDULE, "url")

    def get_hearing_results_base_url(self):
        return self.get_property_value(URLType.HEARING_RESULTS, "url")

    def process_url(self, url):
        try:
            url_obj = urlopen(url)
            if url_obj.status == 200 and 'text/html' in url_obj.getheader('Content-Type'):
                print("Crawled URL:" + url)
                cur_page = url_obj.read().decode('utf-8')
                parsed_content = HTMLParser(cur_page)
                return parsed_content
        except(
                HTTPError, TimeoutError, URLError, SSLError, CertificateError,
                UnicodeDecodeError) as e1:
            print("Exception while crawling URL:\n" + str(e1))
        except Exception as e:
            print("Generic exception while crawling URL:\n" + str(e))
        return None

    def get_monthly_urls_for_hearing_schedules(self):
        base_url = self.get_hearing_schedule_base_url()
        page_contents = self.process_url(base_url)
        return page_contents.get_schedule_links_following_header_string(
            id=self.get_property_value(URLType.HEARING_SCHEDULE, month_h3_id_property_key),
            innerString=self.get_property_value(URLType.HEARING_SCHEDULE,
                                                month_h3_string_property_key))

    def get_monthly_urls_for_hearing_results(self):
        base_url = self.get_hearing_results_base_url()
        page_contents = self.process_url(base_url)
        return page_contents.get_schedule_links_following_header_string(
            innerString=self.get_property_value(URLType.HEARING_RESULTS,
                                                month_h3_string_property_key))

    def get_weekly_urls_for_hearing_results(self):
        base_url = self.get_hearing_results_base_url()
        page_contents = self.process_url(base_url)
        return page_contents.get_schedule_links_following_header_string(
            id=self.get_property_value(URLType.HEARING_RESULTS,
                                       week_h3_id_property_key))
