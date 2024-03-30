from hearing_scraper.pipeline import HearingScraperPipeline


## This is entry point of the application


if __name__ == '__main__':
    print("Hello World")
    latest_data = HearingScraperPipeline().get_latest_data()
    print(latest_data.info())
