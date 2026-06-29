from models.job import Job
from ai.review import AIReview
from ai.base_provider import BaseAIProvider


class MockAIProvider(BaseAIProvider):
    def review_job(self, job: Job) -> AIReview:
        text = f"{job.job_title} {job.job_description}".lower()

        practice_area = "Unknown"

        if "corporate" in text or "m&a" in text or "mergers and acquisitions" in text:
            practice_area = "Corporate"
        elif "patent" in text or "trademark" in text or "intellectual property" in text:
            practice_area = "IP"
        elif "commercial" in text or "contracts" in text:
            practice_area = "Commercial"

        passed = practice_area != "Unknown"

        return AIReview(
            passed=passed,
            decision="PASS" if passed else "REJECT",
            confidence=0.75 if passed else 0.3,
            is_attorney=True,
            seniority="Unknown",
            practice_area=practice_area,
            location_match=True,
            reason=f"Mock AI review detected practice area: {practice_area}",
        )