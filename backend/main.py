from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from . import cv_parser
import io
# import cv_parser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-cv")
async def upload_cv(file: Annotated[UploadFile, File()]):
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        content = await file.read()

        pdf_file = io.BytesIO(content)
        pdf_file.read()
        text = cv_parser.extract_text_from_pdf(pdf_file)

        return {"status": "success", "cv_data": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

    finally:
        await file.seek(0)

# @app.post("/api/save-base-cv/")
# async def save_base_cv(cv_data: ParsedCV):

#     return {"status": "saved"}

# @app.get("/api/get-base-cv")
# async def get_base_cv():


@app.get("/")
def read_root():
    return {"message": "CV Optimizer API"}
