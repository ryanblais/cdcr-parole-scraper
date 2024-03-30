import yaml
from html_parser import *
from enum import Enum
from urllib.request import urlopen
from ssl import SSLError, CertificateError
from urllib.error import HTTPError, URLError

yaml_file_path = "scrapper.yaml"


class URLType(Enum):
    HEARING_SCHEDULE = "hearing_schedule"
    HEARING_RESULTS = "hearing_results"


def get_base_url(urlType: URLType):
    # Return a dictionary of URLs to parse in the next step
    try:
        with open(yaml_file_path, "r") as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print("Error while reading config file: " + str(e))
        raise e
    try:
        if urlType == URLType.HEARING_SCHEDULE:
            return config["hearing-schedules"]["url"]
        elif urlType == URLType.HEARING_RESULTS:
            return config["hearing-results"]["url"]
    except Exception as e:
        print("Error fetching base url: " + str(e))
        raise e


def get_hearing_schedule_base_url():
    return get_base_url(URLType.HEARING_SCHEDULE)


def get_hearing_results_base_url():
    return get_base_url(URLType.HEARING_RESULTS)


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
    return page_contents.get_schedule_links_following_header_string(id="select-a-schedule", innerString="Select a schedule:")


def get_monthly_urls_for_hearing_results():
    base_url = get_hearing_results_base_url()
    page_contents = process_url(base_url)
    return page_contents.get_schedule_links_following_header_string(innerString="Hearing Results by Month:")

