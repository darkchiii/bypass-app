from fastapi import FastAPI, UploadFile, File, HTTPException, Path, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from cv_parser import extract_text_from_pdf
import io
from models import ParsedCV, JobRequirements, JobApplication, Suggestion
from storage import storage
from fastapi.responses import StreamingResponse
from generate_pdf import GeneratePDF, apply_suggestions
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_gen = GeneratePDF()

@app.post("/api/upload-cv")
async def upload_cv(file: Annotated[UploadFile, File()]):
    if not file.content_type == "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        content = await file.read()

        pdf_file = io.BytesIO(content)
        text = extract_text_from_pdf(pdf_file)

        return {"status": "success", "cv_data": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

    finally:
        await file.seek(0)

@app.post("/api/save-base-cv")
async def save_base_cv(cv_data: ParsedCV):

    try:
        storage.save_base_cv(cv_data.name, cv_data)
        return {
            "status": "success",
            "message": "Base CV saved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save CV: {str(e)}"
        )

@app.get("/api/get-base-cv")
async def get_base_cv(user_id: str):
    try:
        cv = storage.get_base_cv(user_id)

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="No base CV found. Please upload and save CV first."
            )
        return cv
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No base CV found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load CV: {str(e)}"
        )

# Base CV preview generator endpoint
@app.post("/api/generate-pdf")
async def preview_pdf(user_id: str = "default"):
    try:
        cv = storage.get_base_cv(user_id)

        if cv is None:
            raise HTTPException(status_code=404, detail="Your base cv was not found.")

        pdf_bytes = pdf_gen.generate_pdf(cv)

        filename = pdf_gen.generate_pdf_name(cv.name, cv.job_title)
        # pdf_gen.convert_html_to_pdf(cv, html_content)

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/api/jobs/create")
async def create_job(job_application: JobApplication = Body(...)):
    """
    Recieving full JobApplication data from frontend after AI analysis
    """
    try:
        storage.save_job_application(
            job_application.user_id,
            job_application.job_id,
            job_application
        )

        return {
            "status": "success",
            "job_id": job_application.job_id
        }

    except Exception as e:
        raise HTTPException(500, f"Failed to save: {str(e)}")

@app.get('/api/jobs/{job_id}')
async def view_job(
        user_id: str = Query(...),
        job_id: str = Path(...)):
    try:
        job_data = storage.get_job_application(user_id, job_id)

        if job_data is None:
            raise HTTPException(
                status_code=404,
                detail="No base data for job application found."
            )

        return job_data

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No job data found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load job data: {str(e)}"
        )


@app.get('/api/jobs')
async def view_jobs(
        user_id: str = Query(...)):
    try:
        all_jobs_data = storage.get_all_jobs(user_id)

        if all_jobs_data is None:
            raise HTTPException(
                status_code=404,
                detail="No base data for job application found."
            )

        return all_jobs_data

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No jobs data found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load jobs data: {str(e)}"
        )

# Update JobApplication
@app.post("/api/jobs/{job_id}/apply_changes")
async def apply_changes(
    job_id: str = Path(...),
    user_id: str = Query(...), #
    changes: List[dict] = Body(...)):

    job_application = storage.get_job_application(user_id, job_id)

    if not job_application:
        raise HTTPException(404, "Job not found")

    for change in changes:
        idx = change["index"]
        job_application.suggestions[idx].status = change["status"]

        if "final_value" in change:
            job_application.suggestions[idx].final_value = change["final_value"]

    job_application.status = "modified"

    storage.save_job_application(user_id, job_id, job_application)

    return {"status": "succes", "message": "Changes applied"}

@app.get("/api/jobs/{job_id}/download")
async def generate_and_download(
    user_id: str = Query(...),
    job_id: str = Path(...),
):
    try:
        job_application = storage.get_job_application(user_id, job_id)
        base_cv = storage.get_base_cv(user_id)

        if not job_application or not base_cv:
            raise HTTPException(404, "Data not found")

        modified_cv = apply_suggestions(base_cv, job_application.suggestions)

        filename = pdf_gen.generate_pdf_name(base_cv.name, job_application.job_requirements.job_title)

        pdf_bytes = pdf_gen.generate_pdf(modified_cv)

        job_application.status = "downloaded"
        storage.save_job_application(user_id, job_id, job_application)

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load jobs data: {str(e)}"
        )


@app.get("/")
def read_root():
    return {"message": "CV Optimizer API"}
