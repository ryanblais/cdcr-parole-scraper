import os
import pandas as pd
from hearing_scraper import HearingScraperPipeline
from case_scraper import CaseScraper


class ScrapeFlow(object):

    def __init__(self, parallel=1):
        google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        self.pipeline = HearingScraperPipeline()
        self.case_scraper = CaseScraper()
        self.results: pd.DataFrame = None
        self.past_actions: pd.DataFrame = []

    def __enter__(self):
        self.case_scraper.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.case_scraper.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, *args, **kwargs):
        self.results = self.pipeline.get_latest_data()
        self.populate_cases()


    def populate_cases(self):
        """
        For each case in the results, get the case details, update results and past_actions
        :return:
        """
        pass

    def publish_speardsheet(self):
        """
        Publish the results to a google sheet
        :return:
        """
        pass


def main():
    flow = ScrapeFlow()
    with flow as f:
        f()


if __name__ == '__main__':
    main()
