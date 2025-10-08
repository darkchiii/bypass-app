import requests
from models import Suggestion, JobApplication, JobRequirements
BASE_URL = "http://localhost:8000"

# # Save parsed CV
# response = requests.post(f"{BASE_URL}/api/save-base-cv", )
# print("Saved Alice:", response.json())

# 2. Get CV
response = requests.get(f"{BASE_URL}/api/get-base-cv?user_id=Alice")
print("Get:", response.json())

# 3. Generate PDF
response = requests.post(f"{BASE_URL}/api/generate-pdf?user_id=Alice")

# if response.status_code == 200:
#     with open("tests/tests_output/downloaded_cv.pdf", "wb") as f:
#         f.write(response.content)
#     print(f"PDF downloaded: {len(response.content)} bytes")
# else:
#     print(f"Error: {response.status_code}")
#     print(response.text)

# # Test Create job 1
# response_job = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application.model_dump())
# job_id = "550e8400-e29b-41d4-a716"
# print("Create job: ", response_job.json())

# # # Test Create job 2
# response_job = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application.model_dump())
# job_id = "520e8400-e29b-41d4-a716"
# print("Create job: ", response_job.json())

# # # Test get job
# # response = requests.get(f"{BASE_URL}/api/jobs/{job_id}?user_id=Lola")
# # print("Get job: ", response.json())

# Test apply changes in job application
alice_job_id = "550e8400-e29b-41d4-a716"
bob_job_id = "abc-def-123-456"
carol_job_id = "xyz-789-ghi-012"

changes = [
    {"index": 0, "status": "accepted"},
    {"index": 1, "status": "accepted"},
    {"index": 2, "status": "accepted"},
    {"index": 3, "status": "accepted"}
]

response = requests.post(f"{BASE_URL}/api/jobs/{alice_job_id}/apply_changes?user_id=Alice", json = changes)
print(response.json())

# Test Download modified CV
response = requests.get(f"{BASE_URL}/api/jobs/{alice_job_id}/download?user_id=Alice")
if response.status_code == 200:
    with open("data/renders/pdf/downloaded_cv.pdf", "wb") as f:
        f.write(response.content)
    print("PDF downloaded!")
else:
    print(f"Error: {response.status_code} - {response.json()}")