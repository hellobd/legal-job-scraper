from filters.base_filter import BaseFilter, FilterResult
from models.job import Job


class LocationFilter(BaseFilter):
    filter_name = "LocationFilter"

    target_locations = [
        "new york",
        "ny",
        "chicago",
        "illinois",
        "houston",
        "dallas",
        "texas",
        "california",
        "san francisco",
        "los angeles",
        "ca",
        "boston",
        "massachusetts",
        "ma",
        "miami",
        "florida",
        "fl",
        "seattle",
        "washington",
        "wa",
        "atlanta",
        "georgia",
        "ga",
    ]

    def apply(self, job: Job) -> FilterResult:
        location = job.location.lower()

        for target in self.target_locations:
            if target in location:
                return FilterResult(
                    passed=True,
                    filter_name=self.filter_name,
                    reason=f"Passed because location matches target market: {target}",
                )

        return FilterResult(
            passed=False,
            filter_name=self.filter_name,
            reason=f"Rejected because location is outside target markets: {job.location}",
        )