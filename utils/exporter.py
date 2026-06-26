import pandas as pd
from models.job import Job
from config.settings import OUTPUT_DIR, OUTPUT_FILE


def export_jobs_to_csv(jobs: list[Job]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not jobs:
        print("No jobs to export.")
        return

    data = [job.to_dict() for job in jobs]

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Exported {len(jobs)} jobs to {OUTPUT_FILE}")