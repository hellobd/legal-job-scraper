LEGAL_JOB_REVIEW_PROMPT = """
You are an experienced legal recruiter.

Review the following job posting and decide whether it matches the client's criteria.

Client criteria:
1. Practicing attorney/lawyer role only.
2. Seniority must be Associate, Attorney, Senior Attorney, Partner, Counsel, or Of Counsel.
3. Location must be one of the target US markets.
4. Practice area must be IP, Commercial, or Corporate.

Return JSON only in this exact structure:

{
  "passed": true,
  "decision": "PASS",
  "confidence": 0.95,
  "is_attorney": true,
  "seniority": "Associate",
  "practice_area": "Corporate",
  "location_match": true,
  "reason": "Short explanation"
}

Job Title:
{job_title}

Location:
{location}

Job Description:
{job_description}
"""