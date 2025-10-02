import pdfplumber
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file"""
    with pdfplumber.open(file_bytes) as pdf:
        text = ""
        for page in pdf.pages:
            text_page = page.extract_text()
            if text_page:
                text += text_page + "\n\n"
    return {"text": text}


# def parse_cv_sections(text: str):
#     """Parsing CV into sections"""
#     sections = {
#         "raw_text": text,
#         "name": "",
#         "bio": "",
#         "job_title": "",
#         "professional experience": "",
#         "skills": "",
#     }

#     return sections
