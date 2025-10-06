import requests

BASE_URL = "http://localhost:8000"


cv_data = {'name': 'Lola', 'email': 'lola@lola.com', 'location': 'Warsaw', 'phone': '678 432 280', 'job_title': 'Python Developer', 'bio': 'Experienced and excellent Lola Loki', 'skills': ['Python', 'Docker', 'DRF'], 'languages': ['English C1', 'Polish native'], 'projects': [{'title': 'Project 1', 'tools': 'xyz zyc', 'description': ['xxxxx', 'yyyyy', 'zzzzz'], 'link': 'https://lola.com'}], 'experience': [{'title': 'Developer X', 'company': 'Company Y', 'date': '05-2021 - 05-2023', 'description': ['xxxxx', 'yyyy', 'zzzz']}], 'education': [{'degree': 'Bachelor', 'field': 'xxx', 'school_name': 'Lola school', 'date': '06-2018 - 09-2020'}]}

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