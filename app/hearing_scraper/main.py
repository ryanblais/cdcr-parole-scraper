import yaml
from html_parser import *
from enum import Enum
from urllib.request import urlopen
from ssl import SSLError, CertificateError
from urllib.error import HTTPError, URLError

property_file_path = "scrapper.yaml"
h3_id_property_key = "h3_id"
h3_string_property_key = "h3_string"


class URLType(Enum):
    HEARING_SCHEDULE = "hearing-schedules"
    HEARING_RESULTS = "hearing-results"


def get_property_value(type: URLType, key: str):
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
        print(config)
        print("Error fetching key value: " + str(e))
        raise e


def get_hearing_schedule_base_url():
    return get_property_value(URLType.HEARING_SCHEDULE, "url")


def get_hearing_results_base_url():
    return get_property_value(URLType.HEARING_RESULTS, "url")


def process_url(url):
    try:
        url_obj = urlopen(url)
        if url_obj.status == 200 and 'text/html' in url_obj.getheader('Content-Type'):
            print("Crawled URL:" + url)
            cur_page = url_obj.read().decode('utf-8')
            parsed_content = HTMLParser(cur_page)
            return parsed_content
    except(HTTPError, TimeoutError, URLError, SSLError, CertificateError, UnicodeDecodeError) as e1:
        print("Exception while crawling URL:\n" + str(e1))
    except Exception as e:
        print("Generic exception while crawling URL:\n" + str(e))
    return None


def get_monthly_urls_for_hearing_schedules():
    base_url = get_hearing_schedule_base_url()
    page_contents = process_url(base_url)
    return page_contents.get_schedule_links_following_header_string(
        id=get_property_value(URLType.HEARING_SCHEDULE, h3_id_property_key),
        innerString=get_property_value(URLType.HEARING_SCHEDULE, h3_string_property_key))


def get_monthly_urls_for_hearing_results():
    base_url = get_hearing_results_base_url()
    page_contents = process_url(base_url)
    return page_contents.get_schedule_links_following_header_string(
        innerString=get_property_value(URLType.HEARING_RESULTS, h3_string_property_key))
