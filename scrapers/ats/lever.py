import requests
from bs4 import BeautifulSoup

from config.settings import HEADERS, REQUEST_TIMEOUT
from models.job import Job
from scrapers.ats.base import BaseScraper
from utils.logger import setup_logger


class LeverScraper(BaseScraper):
    """
    Scraper for Lever-powered job boards.
    Example: https://jobs.lever.co/company
    """

    ats_platform = "Lever"

    def __init__(self, source_url: str):
        super().__init__(source_url)
        self.logger = setup_logger()

    def scrape(self) -> list[Job]:
        html = self._get_listing_page()
        postings = self._parse_listing_page(html)

        total = len(postings)
        self.logger.info(f"Found {total} job cards on listing page.")

        jobs: list[Job] = []

        for index, post in enumerate(postings, start=1):
            job = self._parse_job_card(post)

            if not job:
                continue

            self.logger.info(
                f"[{index}/{total}] Downloading description: {job.job_title}"
            )

            job.job_description = self._get_job_description(job.job_url)
            jobs.append(job)

        return jobs

    def _get_listing_page(self) -> str:
        response = requests.get(
            self.source_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.text

    def _parse_listing_page(self, html: str):
        soup = BeautifulSoup(html, "lxml")
        return soup.select("div.posting")

    def _parse_job_card(self, post) -> Job | None:
        link = post.select_one("a.posting-title")
        title_el = post.select_one("h5[data-qa='posting-name']")
        location_el = post.select_one(".sort-by-location")

        job_url = link.get("href", "").strip() if link else ""
        job_title = title_el.get_text(strip=True) if title_el else ""
        location = location_el.get_text(strip=True) if location_el else ""

        if not job_url or not job_title:
            return None

        return Job(
            job_title=job_title,
            job_url=job_url,
            location=location,
            job_description="",
            source_url=self.source_url,
            ats_platform=self.ats_platform,
        )

    def _get_job_description(self, job_url: str) -> str:
        try:
            response = requests.get(
                job_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            return soup.get_text(" ", strip=True)

        except Exception as e:
            self.logger.warning(f"Could not scrape detail page: {job_url} | {e}")
            return ""