from filters.base_filter import BaseFilter, FilterResult
from models.job import Job


class PracticeAreaFilter(BaseFilter):
    filter_name = "PracticeAreaFilter"

    practice_keywords = {
        "IP": [
            "intellectual property",
            "patent",
            "trademark",
            "copyright",
            "ip litigation",
            "technology transactions",
        ],
        "Corporate": [
            "corporate",
            "m&a",
            "mergers and acquisitions",
            "private equity",
            "venture capital",
            "capital markets",
            "securities",
            "transactional",
        ],
        "Commercial": [
            "commercial",
            "commercial litigation",
            "commercial contracts",
            "business litigation",
            "contract disputes",
        ],
    }

    def apply(self, job: Job) -> FilterResult:
        text = f"{job.job_title} {job.job_description}".lower()

        for area, keywords in self.practice_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return FilterResult(
                        passed=True,
                        filter_name=self.filter_name,
                        reason=f"Passed because job matches practice area: {area} via keyword '{keyword}'",
                    )

        return FilterResult(
            passed=False,
            filter_name=self.filter_name,
            reason="Rejected because job does not match IP, Commercial, or Corporate practice areas",
        )