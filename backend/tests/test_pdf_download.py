# test_pdf_download.py
import requests

response = requests.post("http://localhost:8000/api/generate-pdf?user_id=default")

if response.status_code == 200:
    # with open("data/renders/pdf/downloaded_cv.pdf", "wb") as f:
    #     f.write(response.content)
    print("PDF downloaded!")
else:
    print(f"Error: {response.status_code} - {response.json()}")