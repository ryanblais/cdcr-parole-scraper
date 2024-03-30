import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os


class GoogleSheetsCSVConverter:
    def __init__(self, credentials_path, sheet_name):
        self.credentials_path = credentials_path
        self.sheet_name = sheet_name
        self.client = None
        self.spreadsheet = None

    def load_credentials(self):
        """Load the Google Sheets API credentials."""
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        self.client = gspread.authorize(credentials)

    def convert_csvs_to_sheets(self, csv_file_paths):
        """
        Convert CSV files to separate Google Sheets based on the name of the CSV file.
        :param csv_file_paths: A list of paths to the CSV files.
        """
        if not self.client:
            print("Credentials not loaded. Call load_credentials first.")
            return

        # Open the Google Sheet by name
        self.spreadsheet = self.client.open(self.sheet_name)
        
        # For each CSV file, create or update a sheet with the CSV file name
        for csv_file_path in csv_file_paths:
            # Extract sheet name from the CSV file name
            sheet_title = os.path.splitext(os.path.basename(csv_file_path))[0]
            try:
                # Try to open the sheet if it exists
                sheet = self.spreadsheet.worksheet(sheet_title)
            except gspread.exceptions.WorksheetNotFound:
                # If not found, create a new sheet
                sheet = self.spreadsheet.add_worksheet(title=sheet_title, rows="100", cols="20")
            
            # Clear existing data in the sheet before appending new data
            #sheet.clear()
            
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                # Prepare a list of lists for bulk update to reduce API calls
                rows_to_update = list(csv_reader)
                sheet.append_rows(rows_to_update)
            
            print(f"CSV data from {csv_file_path} has been uploaded to {sheet_title}.")

# Usage example
if __name__ == "__main__":
    # Initialize the converter
    converter = GoogleSheetsCSVConverter('../credentials/my_credentials.json', 'cdcr-parole-googleSheet')
    
  
