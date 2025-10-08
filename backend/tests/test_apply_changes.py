from models import ParsedCV, Project, Education, Experience, Suggestion
from typing import List
from generate_pdf import apply_suggestions
import requests
from models import Suggestion, JobApplication, JobRequirements

BASE_URL = "http://localhost:8000"
# Base CV
base_cv = ParsedCV(name="Lola Loki", email="lola@lola.com", location="Warsaw", phone = "678 432 280", job_title="Python Developer", bio = "Experienced and excellent Lola Loki", skills = ["Python", "Docker", "DRF"], languages=["English C1", "Polish native"],
                  projects = [Project(title="Project 1", tools = "xyz zyc", description = ["xxxxx", "yyyyy", "zzzzz"], link = "https://lola.com")],
    experience=[
        Experience(
            title="Dev",
            company="Corp",
            date="2020-2023",
            description=["Built APIs", "Worked with team"]
        )
    ],
    education = [Education(degree = "Bachelor", field = "xxx", school_name = "Lola school", date = "06-2018 - 09-2020")])
# Sugestie
suggestions = [
    Suggestion(
        type="rewrite",
        section="job_title",
        status="accepted",
        current_value="Python Developer",
        suggested_value="Backend Developer",
        reason="Match job posting"
    ),
    Suggestion(
        type="update_field",
        section="bio",
        status="accepted",
        current_value="Experienced and excellent Lola Loki",
        suggested_value="Experienced and excellent Lola LokiExperienced and excellent Lola Loki",
        reason="Match job posting"
    ),
    Suggestion(
        type="rewrite",
        section="experience",
        target_item_index=0,
        target_field="description",
        target_field_index=1,
        status="accepted",
        current_value="Worked with team",
        suggested_value="Collaborated with cross-functional team",
        reason="Better wording"
    )
]

# Aplikuj
# modified_cv = apply_suggestions(base_cv, suggestions)

# # Sprawdź
# print(modified_cv.job_title)  # "Backend Developer"?
# print(modified_cv.experience[0].description[1])  # "Collaborated..."?
# print(modified_cv)
job_id = "520e8400-e29b-41d4-a716"
response = requests.get(f"{BASE_URL}/api/jobs/{job_id}/download?user_id=Lola")
if response.status_code == 200:
    with open("tests/tests_output/downloaded_cv.pdf", "wb") as f:
        f.write(response.content)
    print(f"PDF downloaded: {len(response.content)} bytes")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
