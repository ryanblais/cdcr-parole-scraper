# Main pipeline class to chain actions

import pandas as pd
from .main import SR_SCRAPER
from datetime import datetime


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
        lastFetchedDate = self.data_scrapper.get_last_fetched_date()
        # Extract month and year
        date = datetime.strptime(lastFetchedDate, '%Y-%m-%d')
        month = date.month
        year = date.year
        print(month, year)


        # get schedule
        urlDict = self.data_scrapper.get_monthly_urls_for_hearing_schedules()
        scheduleData = pd.DataFrame()

        for url in urlDict:
            tempData = self.data_scrapper.getData(urlDict[url])
            scheduleData = pd.concat([scheduleData, tempData], ignore_index=True)

            tempData['SCHEDULED DATE'] = pd.to_datetime(tempData['SCHEDULED DATE'])
            min_date = tempData['SCHEDULED DATE'].min()

        scheduleDataColumns = self.data_scrapper.get_schedule_columns()
        scheduleData = scheduleData[scheduleDataColumns]


        # get result 
        urlDict = self.data_scrapper.get_monthly_urls_for_hearing_results()
        resultData = pd.DataFrame()
        for url in urlDict:
            print(urlDict[url])
            tempData = self.data_scrapper.getData(urlDict[url])
            resultData = pd.concat([resultData, tempData], ignore_index=True)

            tempData['SCHEDULED DATE'] = pd.to_datetime(tempData['SCHEDULED DATE'])
            min_date = tempData['SCHEDULED DATE'].min()

        resultDataColumns = self.data_scrapper.get_result_columns()
        resultData = resultData[resultDataColumns]



        #  merge result
        merge_columns = ['CDC#', 'SCHEDULED DATE']
        for col in scheduleData.columns:
            if col in resultData.columns and col not in merge_columns:
                scheduleData.rename(columns={col: col + '(SCHEDULE TABLE)'}, inplace=True)
                resultData.rename(columns={col: col + '(RESULT TABLE)'}, inplace=True)

        merged_data = pd.merge(scheduleData, resultData, on=merge_columns, how='outer')
        print(merged_data.columns)
        self.data = merged_data
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



