from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from . import cv_parser
# import cv_parser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_cv")
# async def upload_cv(file: UploadFile = File(...)):
async def upload_cv(file: Annotated[UploadFile, File()]):
    # Validate file type
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        content = await file.read()

        # Convert bytes to file-like object for pdfplumber
        # pdf_file = io.BytesIO(content)
        text = cv_parser.extract_text_from_pdf(content)
        sections = cv_parser.parse_cv_sections(text)

        return {"status": "success", "cv_data": sections}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)


@app.get("/")
def read_root():
    return {"message": "CV Optimizer API"}
