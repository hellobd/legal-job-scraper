import requests
from bs4 import BeautifulSoup

from config.settings import HEADERS, REQUEST_TIMEOUT
from models.job import Job
from scrapers.ats.base import BaseScraper


class LeverScraper(BaseScraper):
    """
    Scraper for Lever-powered job boards.
    Example: https://jobs.lever.co/company
    """

    ats_platform = "Lever"

    def scrape(self) -> list[Job]:
        jobs: list[Job] = []

        response = requests.get(
            self.source_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        postings = soup.select("div.posting")

        for post in postings:
            link = post.select_one("a.posting-title")
            title_el = post.select_one("h5[data-qa='posting-name']")
            location_el = post.select_one(".sort-by-location")

            job_url = link.get("href", "").strip() if link else ""
            job_title = title_el.get_text(strip=True) if title_el else ""
            location = location_el.get_text(strip=True) if location_el else ""

            job_description = self._get_job_description(job_url)

            jobs.append(
                Job(
                    job_title=job_title,
                    job_url=job_url,
                    location=location,
                    job_description=job_description,
                    source_url=self.source_url,
                    ats_platform=self.ats_platform,
                )
            )

        return jobs

    def _get_job_description(self, job_url: str) -> str:
        if not job_url:
            return ""

        try:
            response = requests.get(
                job_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            return soup.get_text(" ", strip=True)

        except Exception:
            return ""