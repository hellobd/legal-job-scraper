import pandas as pd

from config.settings import INPUT_FILE
from scrapers.detector import ATSDetector
from utils.logger import setup_logger


def main():
    logger = setup_logger()
    logger.info("Legal Job Scraper started.")

    df = pd.read_csv(INPUT_FILE)

    for source_url in df["url"]:
        logger.info(f"Processing URL: {source_url}")

        scraper = ATSDetector.get_scraper(source_url)

        if scraper is None:
            logger.warning(f"Unsupported ATS or unknown URL: {source_url}")
            continue

        jobs = scraper.scrape()

        logger.info(f"Found {len(jobs)} jobs from {source_url}")

        for job in jobs[:5]:
            logger.info(f"{job.job_title} | {job.location} | {job.job_url}")


if __name__ == "__main__":
    main()