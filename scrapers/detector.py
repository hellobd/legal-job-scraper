from scrapers.ats.base import BaseScraper
from scrapers.ats.lever import LeverScraper


class ATSDetector:
    """
    Detects the ATS platform from a URL
    and returns the correct scraper class.
    """

    @staticmethod
    def get_scraper(source_url: str) -> BaseScraper | None:
        url = source_url.lower()

        if "jobs.lever.co" in url:
            return LeverScraper(source_url)

        return None