from dataclasses import dataclass


@dataclass
class AIReview:
    passed: bool
    decision: str
    confidence: float
    is_attorney: bool
    seniority: str
    practice_area: str
    location_match: bool
    reason: str