import pandas as pd

from config.settings import INPUT_FILE
from scrapers.detector import ATSDetector
from utils.logger import setup_logger
from utils.exporter import export_jobs_to_csv


def main():
    logger = setup_logger()
    logger.info("Legal Job Scraper started.")

    df = pd.read_csv(INPUT_FILE)

    all_jobs = []

    for source_url in df["url"]:
        logger.info(f"Processing URL: {source_url}")

        scraper = ATSDetector.get_scraper(source_url)

        if scraper is None:
            logger.warning(f"Unsupported ATS or unknown URL: {source_url}")
            continue

        try:
            jobs = scraper.scrape()
            all_jobs.extend(jobs)

            logger.info(f"Found {len(jobs)} jobs from {source_url}")

            for job in jobs[:5]:
                logger.info(f"{job.job_title} | {job.location} | {job.job_url}")

        except Exception as e:
            logger.error(f"Failed to scrape {source_url}: {e}")

    export_jobs_to_csv(all_jobs)

    logger.info(f"Total jobs exported: {len(all_jobs)}")
    logger.info("Legal Job Scraper finished.")


if __name__ == "__main__":
    main()