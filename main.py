import time
import pandas as pd

from config.settings import INPUT_FILE
from scrapers.detector import ATSDetector
from utils.logger import setup_logger
from utils.exporter import export_jobs_to_csv
from database.repository import JobRepository, JobSaveResult


def main():
    start_time = time.time()

    logger = setup_logger()
    logger.info("Legal Job Scraper started.")

    repository = JobRepository()
    df = pd.read_csv(INPUT_FILE)

    all_jobs = []

    total_new = 0
    total_updated = 0
    total_unchanged = 0
    total_errors = 0
    urls_processed = 0

    for source_url in df["url"]:
        logger.info(f"Processing URL: {source_url}")

        repository.start_scrape_run(source_url)
        logger.info(f"Started scrape run for source: {source_url}")

        scraper = ATSDetector.get_scraper(source_url)

        if scraper is None:
            logger.warning(f"Unsupported ATS or unknown URL: {source_url}")
            total_errors += 1
            continue

        try:
            jobs = scraper.scrape()
            all_jobs.extend(jobs)
            urls_processed += 1

            logger.info(f"Found {len(jobs)} jobs from {source_url}")

            for job in jobs:
                result = repository.save_job(job)

                if result == JobSaveResult.NEW:
                    total_new += 1
                elif result == JobSaveResult.UPDATED:
                    total_updated += 1
                else:
                    total_unchanged += 1

            for job in jobs[:5]:
                logger.info(f"{job.job_title} | {job.location} | {job.job_url}")

        except Exception as e:
            logger.error(f"Failed to scrape {source_url}: {e}")
            total_errors += 1

    export_jobs_to_csv(all_jobs)

    closed_jobs = repository.get_closed_jobs()
    active_count = repository.get_active_job_count()
    closed_count = repository.get_closed_job_count()

    duration = round(time.time() - start_time, 2)

    logger.info("=" * 60)
    logger.info("LEGAL JOB SCRAPER SUMMARY")
    logger.info("=" * 60)
    logger.info(f"URLs processed: {urls_processed}")
    logger.info(f"Jobs scraped/exported: {len(all_jobs)}")
    logger.info(f"New jobs: {total_new}")
    logger.info(f"Updated jobs: {total_updated}")
    logger.info(f"Unchanged jobs: {total_unchanged}")
    logger.info(f"Active jobs in database: {active_count}")
    logger.info(f"Closed jobs in database: {closed_count}")
    logger.info(f"Errors: {total_errors}")
    logger.info(f"Duration: {duration} seconds")

    if closed_jobs:
        logger.info("Closed jobs:")
        for title, location, url, last_seen in closed_jobs[:10]:
            logger.info(f"- {title} | {location} | Last seen: {last_seen} | {url}")

    logger.info("=" * 60)
    logger.info("Legal Job Scraper finished.")


if __name__ == "__main__":
    main()