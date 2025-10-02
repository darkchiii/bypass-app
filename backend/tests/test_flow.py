import requests

BASE_URL = "http://localhost:8000"

# Upload CV
# files = {'file': open('data/test_cv.pdf', 'rb')}
# response = requests.post(f"{BASE_URL}/api/upload-cv", files=files)
# print("Upload:", response.json())

# Save parsed CV
cv_data = {'name': 'Lola Loki', 'email': 'lola@lola.com', 'location': 'Warsaw', 'phone': '678 432 280', 'job_title': 'Python Developer', 'bio': 'Experienced and excellent Lola Loki', 'skills': ['Python', 'Docker', 'DRF'], 'languages': ['English C1', 'Polish native'], 'projects': [{'title': 'Project 1', 'tools': 'xyz zyc', 'description': ['xxxxx', 'yyyyy', 'zzzzz'], 'link': 'https://lola.com'}], 'experience': [{'title': 'Developer X', 'company': 'Company Y', 'date': '05-2021 - 05-2023', 'description': ['xxxxx', 'yyyy', 'zzzz']}], 'education': [{'degree': 'Bachelor', 'field': 'xxx', 'school_name': 'Lola school', 'date': '06-2018 - 09-2020'}]}
response = requests.post(f"{BASE_URL}/api/save-base-cv/", json=cv_data)
print("Save:", response.json())

# Get Cv
response = requests.get(f"{BASE_URL}/api/get-base-cv")
print("Get:", response.json())
