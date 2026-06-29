from dataclasses import dataclass
from models.job import Job


@dataclass
class FilterResult:
    passed: bool
    filter_name: str
    reason: str


class BaseFilter:
    filter_name = "BaseFilter"

    def apply(self, job: Job) -> FilterResult:
        raise NotImplementedError