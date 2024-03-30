"""
This file is used to parse the detail for CDCR case page.
Usage:
basicInfo, hearingActions = parseHearingInfo(htmlString)
Then, you have basicInfo as a dictionary and hearingActions as a DataFrame.
Author: Nikola Huang
"""
from typing import List
from pandas import DataFrame
from datetime import date

from bs4 import BeautifulSoup


def filterOutEmptyStrings(listWithEmptyCells: List[str]) -> List[str]:
    """
    Filter out empty string or Nones.
    """
    return list(filter(lambda cell: cell, listWithEmptyCells))


def getBasicInfo(soup: BeautifulSoup, interestedProperties: set) -> dict:
    basicInfo = dict()
    # Scrape basic info.
    for propertyAndValueDiv in soup.find_all("div", {"class": "v-row--no-gutters"}):
        propertyAndValue = [classToValueDiv.getText().strip() for classToValueDiv in propertyAndValueDiv]
        # Filter out empty divs.
        propertyAndValue = filterOutEmptyStrings(propertyAndValue)
        if len(propertyAndValue) >= 2 and propertyAndValue[0] in interestedProperties:
            propertyName = propertyAndValue[0]
            value = propertyAndValue[1]
            if propertyName == 'Name':
                [last, first] = value.split(',')
                basicInfo["Last Name"] = last.strip()
                basicInfo["First + Middle Name"] = first.strip()
            else:
                if propertyName == 'CDCR Number':
                    propertyName = 'CDC#'
                # Example: basicInfo['Age'] = 39
                basicInfo[propertyName] = value

    return basicInfo


def getHearingActions(soup: BeautifulSoup, lastName: str, firstName: str, CDCR: str) -> DataFrame:
    """
    Collect the hearing action data and store it into a DataFrame
    Assumption: Hearing action is the only <table> in this page.
    """
    listOfList = []
    for tr in soup.find('table').find_all('tr'):
        allCells = tr.find_all('td')
        if not allCells or not allCells[0]:
            continue
        row = [lastName, firstName, CDCR]
        for cell in allCells:
            row.append(cell.text.strip())
        listOfList.append(row)

    hearingTable = DataFrame(listOfList)
    hearingTable.columns = ['Last Name', 'First + Middle Name', 'CDC#', 'Date', 'Action', 'Status', 'Outcome']
    return hearingTable


def parseHearingInfo(html: str) -> (dict, DataFrame):
    """
    Given a HTML string, return the dictionary containing the basic info. as well as a DataFrame for hearing actions.
    """
    soup = BeautifulSoup(html, 'html.parser')
    basicInfo = getBasicInfo(
        soup,
        {'Name', 'CDCR Number', 'Age', 'Admission Date', 'Parole Eligible Date'}
    )

    hearingActions = getHearingActions(soup, basicInfo['Last Name'], basicInfo['First + Middle Name'], basicInfo['CDC#'])
    basicInfo['Past Hearing Actions # (Count)'] = len(hearingActions) - 1
    basicInfo['Date of CIRIS pull'] = date.today().strftime("%m/%d/%y")
    return basicInfo, hearingActions
