from abc import ABC, abstractmethod
from models.job import Job
from ai.review import AIReview


class BaseAIProvider(ABC):
    @abstractmethod
    def review_job(self, job: Job) -> AIReview:
        pass