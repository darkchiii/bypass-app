import requests
from models import Suggestion, JobApplication, JobRequirements

BASE_URL = "http://localhost:8000"


cv_data = {'name': 'Lola', 'email': 'lola@lola.com', 'location': 'Warsaw', 'phone': '678 432 280', 'job_title': 'Python Developer', 'bio': 'Experienced and excellent Lola Loki', 'skills': ['Python', 'Docker', 'DRF'], 'languages': ['English C1', 'Polish native'], 'projects': [{'title': 'Project 1', 'tools': 'xyz zyc', 'description': ['xxxxx', 'yyyyy', 'zzzzz'], 'link': 'https://lola.com'}], 'experience': [{'title': 'Developer X', 'company': 'Company Y', 'date': '05-2021 - 05-2023', 'description': ['xxxxx', 'yyyy', 'zzzz']}], 'education': [{'degree': 'Bachelor', 'field': 'xxx', 'school_name': 'Lola school', 'date': '06-2018 - 09-2020'}]}
cv_data2 = {'name': 'LolaL', 'email': 'lola@lola.com', 'location': 'Warsaw', 'phone': '678 432 280', 'job_title': 'Python Developer', 'bio': 'Experienced and excellent Lola Loki', 'skills': ['Python', 'Docker', 'DRF'], 'languages': ['English C1', 'Polish native'], 'projects': [{'title': 'Project 1', 'tools': 'xyz zyc', 'description': ['xxxxx', 'yyyyy', 'zzzzz'], 'link': 'https://lola.com'}], 'experience': [{'title': 'Developer X', 'company': 'Company Y', 'date': '05-2021 - 05-2023', 'description': ['xxxxx', 'yyyy', 'zzzz']}], 'education': [{'degree': 'Bachelor', 'field': 'xxx', 'school_name': 'Lola school', 'date': '06-2018 - 09-2020'}]}

# Save parsed CV
response = requests.post(f"{BASE_URL}/api/save-base-cv", json=cv_data)
print("Save:", response.json())

# 2. Get CV
response = requests.get(f"{BASE_URL}/api/get-base-cv?user_id=Lola")
print("Get:", response.json())

# 3. Generate PDF
response = requests.post(f"{BASE_URL}/api/generate-pdf?user_id=Lola")

if response.status_code == 200:
    with open("tests/tests_output/downloaded_cv.pdf", "wb") as f:
        f.write(response.content)
    print(f"PDF downloaded: {len(response.content)} bytes")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Test data
suggestion3 = Suggestion(
    type="add_keyword",
    section="bio",
    target=None,
    current_value="Backend developer with experience in Python",
    suggested_value="Backend developer specializing in Java and scalable enterprise applications",
    reason="Emphasize Java expertise mentioned in job requirements",
    status="pending",
    final_value=None
)

job_reqs = JobRequirements(
    job_title="Senior Java Developer",
    company="XYZ Tech",
    key_skills=["Java", "Spring Boot", "Microservices", "PostgreSQL"],
    important_keywords=["scalable", "enterprise", "agile", "CI/CD"],
    responsibilities=[
        "Design and develop microservices architecture",
        "Collaborate with cross-functional teams",
        "Maintain high code quality standards"
    ],
    company_values=["innovation", "continuous learning", "teamwork"],
    tone="technical"
)

job_application = JobApplication(
    job_id="550e8400-e29b-41d4-a716",
    user_id="Lola",
    job_requirements=job_reqs,
    suggestions=[suggestion3],
    status="pending",
    analysis_model="full"
)

job_application = JobApplication(
    job_id="520e8400-e29b-41d4-a716",
    user_id="Lola",
    job_requirements=job_reqs,
    suggestions=[suggestion3],
    status="pending",
    analysis_model="full"
)

# Test Create job 1
response_job = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application.model_dump())
job_id = "550e8400-e29b-41d4-a716"
print("Create job: ", response_job.json())

# Test Create job 2
response_job = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application.model_dump())
job_id = "520e8400-e29b-41d4-a716"
print("Create job: ", response_job.json())

# # Test save requirements
# response = requests.post(f"{BASE_URL}/api/jobs/{job_id_response}/save-requirements?user_id=Lola",
#                          json=job_reqs.model_dump()) # sending as json in body
# print("Save requirements response: ", response.json())

# # Test save suggestions
# response = requests.post(f"{BASE_URL}/api/jobs/{job_id_response}/save-suggestions?user_id=Lola",
#                          json=suggestion3.model_dump()) # sending as json in body
# print("Save suggestion response: ", response.json())

# Test get job
response = requests.get(f"{BASE_URL}/api/jobs/{job_id}?user_id=Lola")
print("Get job: ", response.json())

# Test get all jobs
response = requests.get(f"{BASE_URL}/api/jobs?user_id=Lola")
print("Get all jobs: ", response.json())

# Test get nonexistent job
response = requests.get(f"{BASE_URL}/api/jobs/{"580e8400-e29b-41d4-a716"}?user_id=Lola")
print("Get job: ", response.json())

# Test get jobs for user with no jobs
response = requests.get(f"{BASE_URL}/api/jobs?user_id=Lolal")
print("Get all jobs: ", response.json())