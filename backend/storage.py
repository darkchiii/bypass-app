import json
from pathlib import Path
from models import Education, Experience, ParsedCV, Suggestion, JobApplication, Project
from typing import List
import logging

logger = logging.getLogger(__name__)

class StorageException(Exception):
    """Base exception for all storage errors"""
    pass

class ResourceNotFoundError(StorageException):
    """Resource not found (CV, job application)"""
    pass

class StorageUnavailableError(StorageException):
    """Storage unavailable (disk full, permission denied, corrupted data)"""
    pass

class Storage:
    def __init__(self):
        self.data_dir = Path("data")
        self.cv_dir = Path("data/cv_json")
        self.jobs_dir = Path("data/jobs")

        try:
            self.data_dir.mkdir(exist_ok=True)
            self.cv_dir.mkdir(exist_ok=True)
            self.jobs_dir.mkdir(exist_ok=True)
        except OSError as e:
            logger.critical(f"Cannot create storage directories: {e}")
            raise StorageUnavailableError(f"Storage initialization failed: {e}")


    def save_base_cv(self, user_id:str, cv: ParsedCV):
        # clean_name = "".join(cv.name.split())
        try:
            filepath = self.cv_dir / f"{user_id}_base_cv.json"
            cv_data = cv.model_dump()

            logger.debug(f"Saving CV to {filepath}")

            with open(filepath, "w", encoding='utf-8') as f:
                json.dump(cv_data, f, indent=2, ensure_ascii=False, default=str)

            logger.debug(f"CV saved succesfully to {filepath}")

        except (OSError, IOError, PermissionError) as e:
            raise StorageUnavailableError(
                f"Cannot save CV for {user_id}: {str(e)}"
            ) from e

    def get_base_cv(self, user_id: str):
        filepath = self.cv_dir / f"{user_id}_base_cv.json"

        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ParsedCV(**data)

        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Cannot read CV for {user_id}: {e}", exc_info=True)
            raise StorageUnavailableError(
                f"Cannot read CV file: {str(e)}"
            ) from e

    def save_job_application(self, user_id, job_id, apllication):
        user_dir = self.jobs_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        filepath = user_dir / f"{job_id}.json"
        application_data = apllication.dict()
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(application_data, f, indent=2, ensure_ascii=False, default=str)
        logger.debug(f"Job application {job_id} saved successfully")

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