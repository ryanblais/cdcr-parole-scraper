import os
import typing
import json
import time
from enum import IntEnum
from playwright.sync_api import sync_playwright, Page
from pathlib import Path


__all__ = ['Scraper']


data_dir = Path(__file__).parent.parent / 'data' / 'playwrite'
os.makedirs(data_dir, exist_ok=True)


class Scraper(object):

    def __init__(self):
        self.playwright = sync_playwright()
        self.context = None
        self.browser = None

    def __enter__(self):
        self.context = self.playwright.__enter__()
        self.browser = self.context.chromium.launch_persistent_context(
            user_data_dir=data_dir,
            java_script_enabled=True,
            headless=False
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context = None
        self.browser = None
        self.playwright.__exit__(exc_type, exc_val, exc_tb)

    def get_case_details(self, case_id) -> dict:
        if not self.browser:
            with self as scr, scr.browser.new_page() as page:
                return self._get_case_details(case_id, page)
        else:
            with self.browser.new_page() as page:
                return self._get_case_details(case_id, page)

    def _get_case_details(self, case_id, page: Page) -> dict:
        page.goto(f"https://apps.cdcr.ca.gov/ciris/")
        states = set()
        while PageState.CASE_PAGE not in states:
            time.sleep(0.5)
            new_state = self._page_states(page)
            if new_state == states:
                page.screenshot(path='stuck.png')
                raise RuntimeError(f'Stuck at state {[str(s.name) for s in new_state]}')
            states = new_state

            if PageState.WEB_TEAM_WELCOME in states:
                page.get_by_text(text="Close", exact=True).click()
                continue
            if PageState.DISCLAIMER_PAGE in states:
                page.get_by_text(text="agree", exact=True).click()
                continue
            if PageState.SEARCH_PAGE in states:
                page.get_by_text(text="CDCR Number", exact=True).click()
                page.query_selector("input[aria-label='CDCR Number']").fill(case_id)
                page.get_by_text(text="search", exact=True).click()
                continue
            if PageState.SEARCH_RESULT_PAGE in states:
                page.goto(f"https://apps.cdcr.ca.gov/ciris/details?cdcrNumber={case_id}")
                continue

        html = page.content()
        return self._parse_page(html)

    def _parse_page(self, html: str) -> dict:
        return {}

    def _page_states(self, page: Page) -> typing.List['PageState']:
        page.wait_for_load_state('load')
        page.wait_for_selector("body")

        states = {
            PageState.WEB_TEAM_WELCOME: page.get_by_text(" CDCR Web Team ", exact=True).count(),
            PageState.DISCLAIMER_PAGE: page.get_by_text("Disclaimer", exact=True).count(),
            PageState.SEARCH_PAGE: page.get_by_text("Search By:", exact=True).count(),
            PageState.SEARCH_RESULT_PAGE: page.get_by_text("Search Result for CDCR Number").count(),
            PageState.CASE_PAGE: page.get_by_text("Parole Eligible Date", exact=True).count(),
        }

        return set([state for state, count in states.items() if count])


class PageState(IntEnum):
    WEB_TEAM_WELCOME = 0
    DISCLAIMER_PAGE = 1
    SEARCH_PAGE = 2
    SEARCH_RESULT_PAGE = 3
    CASE_PAGE = 100


if __name__ == '__main__':
    with Scraper() as scraper:
        result = scraper.get_case_details("G64805")
        Path('output.json').write_text(json.dumps(result, indent=2))
