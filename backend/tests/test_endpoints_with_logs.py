# backend/tests/test_upload_pytest.py
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from main import app
import io
import httpx
# from starlette.testclient import TestClient,
client = TestClient(app)

def test_upload_valid_pdf():
    """Test upload poprawnego PDF"""
    # Odczytaj prawdziwy PDF
    with open("data/base_cv_pdf/AliceJohnson_cv.pdf", "rb") as f:
        pdf_content = f.read()

    files = {"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
    response = client.post("/api/upload-cv", files=files)

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["cv_data"]) > 20


def test_upload_wrong_type():
    """Test upload złego typu pliku"""
    files = {"file": ("test.txt", b"Not a PDF", "text/plain")}
    response = client.post("/api/upload-cv", files=files)

    assert response.status_code == 400
    assert "invalid_file_type" in response.json()["detail"]["error"]


def test_upload_corrupted_pdf():
    """Test upload zepsutego PDF"""
    # Fake PDF (będzie ValueError)
    fake_pdf = b"%PDF-1.4\nCorrupted content"
    files = {"file": ("bad.pdf", io.BytesIO(fake_pdf), "application/pdf")}
    response = client.post("/api/upload-cv", files=files)

    assert response.status_code == 400
    assert "invalid_pdf" in response.json()["detail"]["error"]

#Saving CV
def test_save_valid_cv(test_client):
    """Test zapisywania poprawnego CV"""

    cv_data = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "location": "New York",
        "phone": "+1 555-0123",
        "job_title": "Developer",
        "bio": "Experienced developer",
        "skills": ["Python", "JavaScript"],
        "languages": ["English"],
        "experience": [{  # ✅ Min 1 experience
            "title": "Dev",
            "company": "Corp",
            "date": "2020-2023",
            "description": ["Built apps"]
        }],
        "education": [{  #
            "degree": "BSc",
            "field": "CS",
            "school_name": "MIT",
            "date": "2016-2020"
        }]
    }

    response = test_client.post("/api/save-base-cv", json=cv_data)

    print(f"\nResponse: {response.json()}")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "user_id" in response.json()["data"]


def test_save_invalid_email(test_client):
    """Test z niepoprawnym emailem - Pydantic walidacja"""

    cv_data = {
        "name": "Bob",
        "email": "not-an-email",
        "location": "NYC",
        "phone": "123",
        "job_title": "Dev",
        "bio": "Bio",
        "skills": ["Python"],
        "languages": ["English"],
        "experience": [{"title": "Dev", "company": "X", "date": "2020", "description": ["Work"]}],
        "education": [{"degree": "BSc", "field": "CS", "school_name": "MIT", "date": "2020"}]
    }

    response = test_client.post("/api/save-base-cv", json=cv_data)

    print(f"\nResponse: {response.json()}")

    assert response.status_code == 422  # Pydantic validation error
    assert "email" in str(response.json()).lower()


# def test_save_empty_skills(test_client):
#     """Test z pustą listą skills - Pydantic walidacja
#     Nie
#     """

#     cv_data = {
#         "name": "Charlie",
#         "email": "charlie@example.com",
#         "location": "LA",
#         "phone": "555",
#         "job_title": "Dev",
#         "bio": "Bio",
#         "skills": [],  #  Empty list
#         "languages": ["English"],
#         "experience": [{"title": "Dev", "company": "X", "date": "2020", "description": ["Work"]}],
#         "education": [{"degree": "BSc", "field": "CS", "school_name": "MIT", "date": "2020"}]
#     }

#     response = test_client.post("/api/save-base-cv", json=cv_data)

#     print(f"\n Response: {response.json()}")

#     assert response.status_code == 422
#     assert "skills" in str(response.json()).lower()