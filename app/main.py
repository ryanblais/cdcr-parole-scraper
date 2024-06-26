import os
import pandas as pd
from .hearing_scraper import HearingScraperPipeline
from .case_scraper import CaseScraper
from .sheet_exporter import GoogleSheetsCSVConverter
from dotenv import load_dotenv

class ScrapeFlow(object):

    def __init__(self, parallel=1):
        # Load the .env file
        load_dotenv()
        google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        google_sheet_name = os.getenv('GOOGLE_SHEET_NAME')

        self.max_cases = int(os.getenv('MAX_CASES', 10))
        self.sheet_exporter = GoogleSheetsCSVConverter(google_credentials, google_sheet_name)
        self.pipeline = HearingScraperPipeline()
        self.case_scraper = CaseScraper()
        self.results: pd.DataFrame = None
        self.past_actions: pd.DataFrame = None

    def __enter__(self):
        self.case_scraper.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.case_scraper.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, *args, **kwargs):
        print("Start scraping hearing schedule")
        self.results = self.pipeline.get_latest_data()
        self.populate_cases()
        self.dump_to_csv()
        self.publish_speardsheet()
        print("Finish scraping hearing schedule")

    def populate_cases(self):
        """
        For each case in the results, get the case details, update results and past_actions
        :return:
        """
        print("Start scraping cases details")
        cdcr_numbers = self.results['CDC#'].unique()
        past_actions = []
        cases_details = []

        for i, cdcr_number in enumerate(cdcr_numbers):
            print(f"Scraping case details for {i} / {len(cdcr_numbers)}")
            case_details, case_past_actions = self.case_scraper.get_case_details(cdcr_number)
            past_actions.append(case_past_actions)
            cases_details.append(case_details)

            if i > self.max_cases:
                break

        print("Finish scraping cases details")
        self.past_actions = pd.concat(past_actions, ignore_index=True)
        self.results = pd.merge(self.results, pd.DataFrame(cases_details), how='left', on='CDC#')

    def dump_to_csv(self):
        if isinstance(self.results, pd.DataFrame):
            self.results.to_csv('app/csvData/results.csv')

        if isinstance(self.past_actions, pd.DataFrame):
            self.past_actions.to_csv('app/csvData/past_actions.csv')

    def publish_speardsheet(self):
        """
        Publish the results to a google sheet
        :return:
        """
        # Load the credentials
        self.sheet_exporter.load_credentials()
    
        # Convert the CSV files and append their contents to separate sheets
        csv_files = ['app/csvData/results.csv', 'app/csvData/past_actions.csv']
        self.sheet_exporter.convert_csvs_to_sheets(csv_files)
        print("Publishing results to google sheet")


def main():
    flow = ScrapeFlow()
    with flow as f:
        f()


if __name__ == '__main__':
    main()
