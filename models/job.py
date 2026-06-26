from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Job:
    job_title: str
    job_url: str
    location: str
    job_description: str
    source_url: str
    ats_platform: str
    salary: str = ""
    date_posted: str = ""
    status: str = "open"
    date_scraped: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return asdict(self)