import json
from pathlib import Path
from models import Education, Experience, ParsedCV, Project

class Storage:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.cv_dir = Path("data/cv")
        self.cv_dir.mkdir(exist_ok=True)

    def save_base_cv(self, user_id:str, cv: ParsedCV):
        filepath = self.cv_dir / f"{user_id}_base_cv.json"
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

storage = Storage()

# cv = storage.get_base_cv()
# print(cv)
# print(cv.name)