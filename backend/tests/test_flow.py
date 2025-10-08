import requests
from models import Suggestion, JobApplication, JobRequirements, ParsedCV
BASE_URL = "http://localhost:8000"
"""
Happy path test - pełny flow od uploadu CV do downloadu customized PDF
"""

def test_happy_path_full_flow():
    """Test full flow: Upload → Save → Create Job → Apply Changes → Download"""

    print("\n" + "="*60)
    print("HAPPY PATH TEST - Full Flow")
    print("="*60)

    # ==========================================
    # STEP 1: Upload CV (PDF → text)
    # ==========================================
    print("\n[1/7] Uploading CV PDF...")

    with open("data/base_cv_pdf/AliceJohnson_cv.pdf", "rb") as f:
        files = {"file": ("test_cv.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/api/upload-cv", files=files)

    assert response.status_code == 200, f"Upload failed: {response.status_code}"
    assert "cv_data" in response.json(), "No cv_data in response"
    print("CV uploaded and text extracted")


    # ==========================================
    # STEP 2: Save base CV (parsed data)
    # ==========================================
    print("\n[2/7] Saving base CV...")

    alice_cv = {
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "location": "New York, NY",
        "phone": "+1 555-0123",
        "job_title": "Full Stack Developer",
        "bio": "Experienced software developer with 5 years of experience.",
        "skills": ["JavaScript", "React", "Node.js", "Python"],
        "languages": ["English - Native", "Spanish - B2"],
        "projects": [
            {
                "title": "E-commerce Platform",
                "tools": "React, Node.js, MongoDB",
                "description": ["Built complete e-commerce solution", "Implemented payment processing"],
                "link": "https://github.com/alice/ecommerce"
            }
        ],
        "experience": [
            {
                "title": "Full Stack Developer",
                "company": "Tech Solutions Inc",
                "date": "2021 - Present",
                "description": [
                    "Developed web applications using React and Node.js",
                    "Collaborated with design team on UI/UX improvements"
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
        ]
    }

    response = requests.post(f"{BASE_URL}/api/save-base-cv", json=alice_cv)
    assert response.status_code == 200, f"Save CV failed: {response.json()}"
    assert response.json()["status"] == "success"
    print("Base CV saved")


    # ==========================================
    # STEP 3: Get base CV (verify save)
    # ==========================================
    print("\n[3/7] Retrieving saved CV...")

    user_id = "AliceJohnson"  # Clean name
    response = requests.get(f"{BASE_URL}/api/get-base-cv?user_id={user_id}")

    assert response.status_code == 200, f"Get CV failed: {response.status_code}"
    retrieved_cv = response.json()
    assert retrieved_cv["name"] == "Alice Johnson"
    assert retrieved_cv["email"] == "alice.johnson@email.com"
    print("CV retrieved successfully")


    # ==========================================
    # STEP 4: Generate base CV PDF (preview)
    # ==========================================
    print("\n[4/7] Generating base CV PDF preview...")

    response = requests.post(f"{BASE_URL}/api/generate-pdf?user_id={user_id}")

    assert response.status_code == 200, f"PDF generation failed: {response.status_code}"
    assert len(response.content) > 0, "PDF is empty"
    print(f"Base PDF generated: {len(response.content)} bytes")


    # ==========================================
    # STEP 5: Create job application
    # ==========================================
    print("\n[5/7] Creating job application...")

    job_application = {
        "job_id": "550e8400-test-happy-path",
        "user_id": "Alice",
        "job_requirements": {
            "job_title": "Senior React Developer",
            "company": "InnovateTech",
            "key_skills": ["React", "TypeScript", "GraphQL"],
            "important_keywords": ["scalable", "performance"],
            "responsibilities": ["Lead frontend development"],
            "company_values": ["innovation"],
            "tone": "technical"
        },
        "suggestions": [
            {
                "type": "update_field",
                "section": "job_title",
                "current_value": "Full Stack Developer",
                "suggested_value": "Senior React Developer",
                "reason": "Match job posting title",
                "status": "pending"
            },
            {
                "type": "rewrite",
                "section": "bio",
                "current_value": "Experienced software developer with 5 years of experience.",
                "suggested_value": "Senior React developer with 5+ years building scalable applications.",
                "reason": "Emphasize React and scalability",
                "status": "pending"
            },
            {
                "type": "rewrite",
                "section": "experience",
                "target_item_index": 0,
                "target_field": "description",
                "target_field_index": 0,
                "current_value": "Developed web applications using React and Node.js",
                "suggested_value": "Architected scalable web applications using React",
                "reason": "Add scalability keyword",
                "status": "pending"
            }
        ],
        "status": "pending",
        "analysis_model": "full"
    }

    response = requests.post(f"{BASE_URL}/api/jobs/create", json=job_application)
    assert response.status_code == 200, f"Create job failed: {response.json()}"
    job_id = response.json()["job_id"]
    assert job_id == "550e8400-test-happy-path"
    print(f"Job created: {job_id}")


    # ==========================================
    # STEP 6: Apply changes (accept suggestions)
    # ==========================================
    print("\n[6/7] Applying changes to suggestions...")

    changes = [
        {"index": 0, "status": "accepted"},  # Accept job_title change
        {"index": 1, "status": "accepted"},  # Accept bio change
        {"index": 2, "status": "modified", "final_value": "Architected and deployed scalable React applications"}  # Modified
    ]

    response = requests.post(
        f"{BASE_URL}/api/jobs/{job_id}/apply_changes?user_id=Alice",
        json=changes
    )

    assert response.status_code == 200, f"Apply changes failed: {response.json()}"
    assert response.json()["status"] == "succes"  # Note: typo in your code
    print("Changes applied (2 accepted, 1 modified)")


    # ==========================================
    # STEP 7: Download customized CV PDF
    # ==========================================
    print("\n[7/7] Downloading customized CV PDF...")

    response = requests.get(f"{BASE_URL}/api/jobs/{job_id}/download?user_id=Alice")

    assert response.status_code == 200, f"Download failed: {response.status_code}"
    assert len(response.content) > 0, "Downloaded PDF is empty"

    # Save to file
    output_path = "tests/tests_output/happy_path_customized_cv.pdf"
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Customized PDF downloaded: {len(response.content)} bytes")
    print(f"Saved to: {output_path}")


    # ==========================================
    # STEP 8: Verify job status changed
    # ==========================================
    print("\n[BONUS] Verifying job status...")

    response = requests.get(f"{BASE_URL}/api/jobs/{job_id}?user_id=Alice")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["status"] == "downloaded", f"Expected 'downloaded', got '{job_data['status']}'"
    print("Job status updated to 'downloaded'")


    # ==========================================
    # SUCCESS!
    # ==========================================
    print("\n" + "="*60)
    print("HAPPY PATH TEST PASSED - All 7 steps successful!")
    print("="*60 + "\n")


# if __name__ == "__main__":
try:
    test_happy_path_full_flow()
except AssertionError as e:
    print(f"\nTEST FAILED: {e}\n")
    raise
except Exception as e:
    print(f"\nUNEXPECTED ERROR: {e}\n")
    raise

