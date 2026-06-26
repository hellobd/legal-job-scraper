from abc import ABC, abstractmethod
from models.job import Job


class BaseScraper(ABC):
    """
    Base class for all ATS scrapers.

    Every ATS scraper must implement the scrape() method
    and return a list of Job objects.
    """

    def __init__(self, source_url: str):
        self.source_url = source_url

    @abstractmethod
    def scrape(self) -> list[Job]:
        pass