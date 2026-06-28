from datetime import datetime
from models.job import Job
from database.database import Database


class JobSaveResult:
    NEW = "NEW"
    UPDATED = "UPDATED"
    UNCHANGED = "UNCHANGED"


class JobRepository:
    def __init__(self):
        self.db = Database()
        self.db.initialize()

    def start_scrape_run(self, source_url: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                UPDATE jobs
                SET is_active = 0,
                    status = 'closed'
                WHERE source_url = ?
                """,
                (source_url,)
            )

    def save_job(self, job: Job) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.db.connect() as conn:
            existing = conn.execute(
                """
                SELECT job_title, location, job_description, salary, date_posted
                FROM jobs
                WHERE job_url = ?
                """,
                (job.job_url,)
            ).fetchone()

            if not existing:
                conn.execute(
                    """
                    INSERT INTO jobs (
                        job_url, job_title, location, job_description,
                        source_url, ats_platform, salary, date_posted,
                        status, first_seen, last_seen, is_active
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, 1)
                    """,
                    (
                        job.job_url,
                        job.job_title,
                        job.location,
                        job.job_description,
                        job.source_url,
                        job.ats_platform,
                        job.salary,
                        job.date_posted,
                        now,
                        now,
                    )
                )
                return JobSaveResult.NEW

            old_title, old_location, old_description, old_salary, old_date_posted = existing

            has_changed = (
                old_title != job.job_title
                or old_location != job.location
                or old_description != job.job_description
                or old_salary != job.salary
                or old_date_posted != job.date_posted
            )

            conn.execute(
                """
                UPDATE jobs
                SET job_title = ?,
                    location = ?,
                    job_description = ?,
                    source_url = ?,
                    ats_platform = ?,
                    salary = ?,
                    date_posted = ?,
                    status = 'open',
                    last_seen = ?,
                    is_active = 1
                WHERE job_url = ?
                """,
                (
                    job.job_title,
                    job.location,
                    job.job_description,
                    job.source_url,
                    job.ats_platform,
                    job.salary,
                    job.date_posted,
                    now,
                    job.job_url,
                )
            )

            return JobSaveResult.UPDATED if has_changed else JobSaveResult.UNCHANGED

    def get_active_job_count(self, source_url: str | None = None) -> int:
        with self.db.connect() as conn:
            if source_url:
                return conn.execute(
                    "SELECT COUNT(*) FROM jobs WHERE is_active = 1 AND source_url = ?",
                    (source_url,)
                ).fetchone()[0]

            return conn.execute(
                "SELECT COUNT(*) FROM jobs WHERE is_active = 1"
            ).fetchone()[0]

    def get_closed_job_count(self, source_url: str | None = None) -> int:
        with self.db.connect() as conn:
            if source_url:
                return conn.execute(
                    "SELECT COUNT(*) FROM jobs WHERE is_active = 0 AND source_url = ?",
                    (source_url,)
                ).fetchone()[0]

            return conn.execute(
                "SELECT COUNT(*) FROM jobs WHERE is_active = 0"
            ).fetchone()[0]

    def get_closed_jobs(self, source_url: str | None = None):
        with self.db.connect() as conn:
            if source_url:
                return conn.execute(
                    """
                    SELECT job_title, location, job_url, last_seen
                    FROM jobs
                    WHERE is_active = 0 AND source_url = ?
                    ORDER BY last_seen DESC
                    """,
                    (source_url,)
                ).fetchall()

            return conn.execute(
                """
                SELECT job_title, location, job_url, last_seen
                FROM jobs
                WHERE is_active = 0
                ORDER BY last_seen DESC
                """
            ).fetchall()