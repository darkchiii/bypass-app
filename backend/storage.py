import json
from pathlib import Path
from models import Education, Experience, ParsedCV, Suggestion, JobApplication, Project
from typing import List

class Storage:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.cv_dir = Path("data/cv_json")
        self.cv_dir.mkdir(exist_ok=True)
        self.jobs_dir = Path("data/jobs")
        self.jobs_dir.mkdir(exist_ok=True)

    def save_base_cv(self, user_id:str, cv: ParsedCV):
        clean_name = "".join(cv.name.split())
        filepath = self.cv_dir / f"{clean_name}_base_cv.json"
        cv_data = cv.dict()
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(cv_data, f, indent=2, ensure_ascii=False, default=str)

    def get_base_cv(self, user_id: str):
        filepath = self.cv_dir / f"{user_id}_base_cv.json"
        if not filepath.exists():
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return ParsedCV(**data)

    def save_job_application(self, user_id, job_id, apllication):
        user_dir = self.jobs_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        filepath = user_dir / f"{job_id}.json"
        application_data = apllication.dict()
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(application_data, f, indent=2, ensure_ascii=False, default=str)

    def get_job_application(self, user_id, job_id):
        filepath = self.jobs_dir / str(user_id) / f"{job_id}.json"
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
        return JobApplication(**data)

    def get_all_jobs(self, user_id):
        user_dir = self.jobs_dir / str(user_id)
        if not user_dir.exists():
            return []

        jobs = []
        for job_file in user_dir.glob("*.json"):
            try:
                with open(job_file, "r", encoding="utf-8") as f:
                    job_data = json.load(f)

                # Check if JobApplication
                if "job_id" not in job_data:
                    print(f"Skipping invalid file: {job_file.name} (missing job_id)")
                    continue

                jobs.append(JobApplication(**job_data))

            except (json.JSONDecodeError, OSError) as e:
                print(f"Error reading {job_file.name}: {e}")
                continue

            except Exception as e:
                print(f"Invalid JobApplication format in {job_file.name}: {e}")
                continue

        return jobs

storage = Storage()