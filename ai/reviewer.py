from models.job import Job
from ai.base_provider import BaseAIProvider
from ai.review import AIReview


class AIReviewer:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider

    def review(self, job: Job) -> AIReview:
        return self.provider.review_job(job)