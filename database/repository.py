from datetime import datetime
from models.job import Job
from database.database import Database


class JobRepository:
    def __init__(self):
        self.db = Database()
        self.db.initialize()

    def save_job(self, job: Job) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.db.connect() as conn:
            existing = conn.execute(
                "SELECT id FROM jobs WHERE job_url = ?",
                (job.job_url,)
            ).fetchone()

            if existing:
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
            else:
                conn.execute(
                    """
                    INSERT INTO jobs (
                        job_url,
                        job_title,
                        location,
                        job_description,
                        source_url,
                        ats_platform,
                        salary,
                        date_posted,
                        status,
                        first_seen,
                        last_seen,
                        is_active
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

    def get_active_jobs(self):
        with self.db.connect() as conn:
            return conn.execute(
                "SELECT * FROM jobs WHERE is_active = 1"
            ).fetchall()