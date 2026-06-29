from filters.base_filter import BaseFilter, FilterResult
from models.job import Job


class SeniorityFilter(BaseFilter):
    filter_name = "SeniorityFilter"

    allowed_keywords = [
        "associate",
        "attorney",
        "senior attorney",
        "partner",
        "counsel",
        "of counsel",
    ]

    rejected_keywords = [
        "law clerk",
        "paralegal",
        "legal assistant",
        "legal secretary",
        "intern",
        "summer associate",
        "trainee",
        "student",
    ]

    def apply(self, job: Job) -> FilterResult:
        text = f"{job.job_title} {job.job_description}".lower()

        for keyword in self.rejected_keywords:
            if keyword in text:
                return FilterResult(
                    passed=False,
                    filter_name=self.filter_name,
                    reason=f"Rejected because seniority/title contains disallowed keyword: {keyword}",
                )

        for keyword in self.allowed_keywords:
            if keyword in text:
                return FilterResult(
                    passed=True,
                    filter_name=self.filter_name,
                    reason=f"Passed because seniority matches allowed keyword: {keyword}",
                )

        return FilterResult(
            passed=False,
            filter_name=self.filter_name,
            reason="Rejected because seniority level is not Associate, Attorney, Senior Attorney, Partner, or Counsel",
        )