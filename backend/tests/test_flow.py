import requests
from models import Suggestion, JobApplication, JobRequirements, ParsedCV
BASE_URL = "http://localhost:8000"

# Upload and parse CV data
with open("tests/tests_output/downloaded_cv.pdf", "rb") as f:
    files = {"file": ("downloaded_cv.pdf", f, "application/pdf")}
    response = requests.post(f"{BASE_URL}/api/upload-cv", files=files)
    # alice_cv_data = response.json()["cv_data"]
    # print(f"alice: ", alice_cv_data)
print("Parsed Alice cv:", response.json())

# AI parsing CV to sections...
Alice ={
  "name": "Alice Johnson",
  "email": "alice.johnson@email.com",
  "location": "New York, NY",
  "phone": "+1 555-0123",
  "job_title": "Full Stack Developer",
  "bio": "Experienced software developer with 5 years of experience in web development. Passionate about creating efficient and scalable applications.",
  "skills": [
    "JavaScript",
    "React",
    "Node.js",
    "Python",
    "PostgreSQL",
    "Docker"
  ],
  "languages": [
    "English - Native",
    "Spanish - B2"
  ],
  "projects": [
    {
      "title": "E-commerce Platform",
      "tools": "React, Node.js, MongoDB",
      "description": [
        "Built complete e-commerce solution",
        "Implemented payment processing",
        "Created admin dashboard"
      ],
      "link": "https://github.com/alice/ecommerce"
    },
    {
      "title": "Task Management App",
      "tools": "Vue.js, Express, MySQL",
      "description": [
        "Developed real-time collaboration features",
        "Integrated email notifications",
        "Optimized database queries"
      ],
      "link": "https://github.com/alice/taskapp"
    }
  ],
  "experience": [
    {
      "title": "Full Stack Developer",
      "company": "Tech Solutions Inc",
      "date": "2021 - Present",
      "description": [
        "Developed web applications using React and Node.js",
        "Collaborated with design team on UI/UX improvements",
        "Implemented automated testing with Jest",
        "Reduced page load time by 40%"
      ]
    },
    {
      "title": "Junior Developer",
      "company": "StartupXYZ",
      "date": "2019 - 2021",
      "description": [
        "Built RESTful APIs",
        "Worked with MongoDB and Express",
        "Participated in code reviews"
      ]
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "school_name": "State University",
      "date": "2015 - 2019"
    }
  ]}

# # Save parsed CV
response = requests.post(f"{BASE_URL}/api/save-base-cv", json=Alice)
print("Saved Alice:", response.json())

# # Get CV
response = requests.get(f"{BASE_URL}/api/get-base-cv?user_id=AliceJohnson")
print("Get:", response.json())

# # Generate PDF
response = requests.post(f"{BASE_URL}/api/generate-pdf?user_id=AliceJohnson")

if response.status_code == 200:
    with open(f"data/base_cv_pdf/{Alice["name"]}_cv.pdf", "wb") as f:
        f.write(response.content)
    print(f"PDF downloaded: {len(response.content)} bytes")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# # Test Create job 1
job_application_alice_1 = {
  "job_id": "550e8400-e29b-41d4-a716",
  "user_id": "Alice",
  "job_requirements": {
    "job_title": "Senior React Developer",
    "company": "InnovateTech",
    "key_skills": [
      "React",
      "TypeScript",
      "GraphQL",
      "AWS"
    ],
    "important_keywords": [
      "scalable",
      "performance",
      "modern web",
      "microservices"
    ],
    "responsibilities": [
      "Lead frontend development",
      "Mentor junior developers",
      "Architect scalable solutions"
    ],
    "company_values": [
      "innovation",
      "continuous learning",
      "collaboration"
    ],
    "tone": "technical"
  },
  "suggestions": [
    {
      "type": "update_field",
      "section": "job_title",
    #   "target_item_index": null,
    #   "target_field": null,
    #   "target_field_index": null,
      "current_value": "Full Stack Developer",
      "suggested_value": "Senior React Developer",
      "reason": "Match job posting title for better ATS alignment",
      "status": "accepted",
    #   "final_value": null
    },
    {
      "type": "rewrite",
      "section": "bio",
    #   "target_item_index": null,
    #   "target_field": null,
    #   "target_field_index": null,
      "current_value": "Experienced software developer with 5 years of experience in web development. Passionate about creating efficient and scalable applications.",
      "suggested_value": "Senior React developer with 5 years of experience building scalable web applications. Specialized in modern frontend architecture and performance optimization.",
      "reason": "Emphasize React expertise and scalability keywords from job posting",
      "status": "accepted",
      "final_value": "Senior React developer with 5+ years of experience building high-performance, scalable web applications. Expert in modern frontend architecture with focus on React ecosystem."
    },
    {
      "type": "rewrite",
      "section": "experience",
      "target_item_index": 0,
      "target_field": "description",
      "target_field_index": 0,
      "current_value": "Developed web applications using React and Node.js",
      "suggested_value": "Architected and developed scalable web applications using React, focusing on performance optimization and modern best practices",
      "reason": "Add scalability and performance keywords",
      "status": "accepted",
    #   "final_value": null
    },
    {
      "type": "rewrite",
      "section": "experience",
      "target_item_index": 0,
      "target_field": "description",
      "target_field_index": 1,
      "current_value": "Collaborated with design team on UI/UX improvements",
      "suggested_value": "Led cross-functional collaboration with design team to deliver exceptional user experiences",
      "reason": "Show leadership alignment with Senior role",
      "status": "accepted",
    #   "final_value": null
    }
  ],
  "status": "downloaded",
  "analysis_model": "full"
}
response_job = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application_alice_1)
print(response_job.json())

# # Test get job
job_id = '550e8400-e29b-41d4-a716'
response = requests.get(f"{BASE_URL}/api/jobs/{job_id}?user_id=Alice")
print("Get job: ", response.json())

# Test apply changes in job application

changes = [
    {"index": 0, "status": "accepted"},
    {"index": 1, "status": "accepted"},
    {"index": 2, "status": "accepted"},
    {"index": 3, "status": "accepted"}
]

response = requests.post(f"{BASE_URL}/api/jobs/{job_id}/apply_changes?user_id=Alice", json = changes)
print(response.json())

# Test Download modified CV
response = requests.get(f"{BASE_URL}/api/jobs/{job_id}/download?user_id=Alice")
if response.status_code == 200:
    with open(f"data/renders/pdf/{Alice["name"]}.pdf", "wb") as f:
        f.write(response.content)
    print("PDF downloaded!")
else:
    print(f"Error: {response.status_code} - {response.json()}")