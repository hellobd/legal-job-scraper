from filters.base_filter import BaseFilter, FilterResult
from models.job import Job


class TitleFilter(BaseFilter):
    filter_name = "TitleFilter"

    keep_keywords = [
        "attorney",
        "associate",
        "senior attorney",
        "partner",
        "counsel",
        "of counsel",
    ]

    discard_keywords = [
        "paralegal",
        "legal assistant",
        "legal secretary",
        "law clerk",
        "intern",
        "summer associate",
        "marketing",
        "sales",
        "finance",
        "hr",
        "human resources",
        "it",
        "operations",
        "business development",
    ]

    def apply(self, job: Job) -> FilterResult:
        title = job.job_title.lower()

        for keyword in self.discard_keywords:
            if keyword in title:
                return FilterResult(
                    passed=False,
                    filter_name=self.filter_name,
                    reason=f"Rejected because title contains discard keyword: {keyword}",
                )

        for keyword in self.keep_keywords:
            if keyword in title:
                return FilterResult(
                    passed=True,
                    filter_name=self.filter_name,
                    reason=f"Passed because title contains attorney keyword: {keyword}",
                )

        return FilterResult(
            passed=False,
            filter_name=self.filter_name,
            reason="Rejected because title does not look like an attorney role",
        )