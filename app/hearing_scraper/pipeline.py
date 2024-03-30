# Main pipeline class to chain actions

import pandas as pd
from .main import SR_SCRAPER


class HearingScraperPipeline:
    data = None
    data_scrapper = None
    

    def __init__(self):
        self.data = pd.DataFrame()
        self.data_scrapper = SR_SCRAPER()

    def get_latest_data(self) -> pd.DataFrame:
        """
        Do the following:
        1. Fetch the latest copy of the master Google sheet

        2. Scrape the hearing schedule page and get the URLs
        3. Scrape each URL, sync against the master sheet & add rows if available
        4. Scrape the hearing results page and get the URLs
        5. Append to the existing rows with additional data
        6. Return the final dataset (as a Pandas#DataFrame)
        :return: pd.DataFrame
        """
        # 2
        urlDict = self.data_scrapper.get_monthly_urls_for_hearing_schedules()
        print(urlDict)
        for url in urlDict:
            tempData = self.data_scrapper.getData(urlDict[url])
            if self.data.empty:
                self.data = tempData
            else:
                self.data = pd.concat([self.data, tempData], ignore_index=True).reset_index(drop=True)
            print(self.data.shape)
        
        urlDict = self.data_scrapper.get_monthly_urls_for_hearing_results()

        return self.data


class DummyData:

    def __init__(self):
        # Define the data as a list of lists
        # Define the columns from both indexes
        columns = ['OFFENDER NAME', 'CDC#', 'HEARING TYPE', 'COUNTY OF COMMITMENT',
                   'PANEL', 'HEARING LOCATION', 'HEARING METHOD', 'SCHEDULED DATE',
                   'HEARING TIME', 'COUNTY OF COMMITMENT', 'GOV CODE', 'RESULT']

        # Define dummy data for two rows
        data = [
            ['John Doe', '12345', 'Initial Hearing', 'Los Angeles', 'Panel A', 'Courtroom 1',
             'In-person', '2024-03-01', '9:00 AM', 'Los Angeles', 'PC 3041.2', 'Grant'],
            ['Jane Smith', '67890', 'Rehearing', 'San Francisco', 'Panel B', 'Courtroom 2',
             'Virtual', '2024-03-15', '2:00 PM', 'San Francisco', None, 'Waive 1 yr']
        ]

        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Create the DataFrame
        self.df = pd.DataFrame(data, columns=columns)

    def get(self):
        return self.df




# HearingScraperPipeline().get_latest_data()



