from filters.base_filter import FilterResult
from filters.title_filter import TitleFilter
from filters.seniority_filter import SeniorityFilter
from filters.location_filter import LocationFilter
from filters.practice_area_filter import PracticeAreaFilter
from models.job import Job


class FilterManager:
    def __init__(self):
        self.filters = [
            TitleFilter(),
            SeniorityFilter(),
            LocationFilter(),
            PracticeAreaFilter(),
        ]

    def apply_filters(self, job: Job) -> tuple[bool, list[FilterResult]]:
        results = []

        for job_filter in self.filters:
            result = job_filter.apply(job)
            results.append(result)

            if not result.passed:
                return False, results

        return True, results