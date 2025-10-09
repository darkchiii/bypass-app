import re
from fastapi import FastAPI, UploadFile, File, HTTPException, Path, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from cv_parser import extract_text_from_pdf
import io
from models import ParsedCV, JobRequirements, JobApplication, Suggestion
from storage import storage, StorageUnavailableError
from fastapi.responses import StreamingResponse
from generate_pdf import GeneratePDF, apply_suggestions
from typing import List
import logging

app = FastAPI()
pdf_gen = GeneratePDF()

logging.basicConfig(
    level=logging.DEBUG,  # prod: info, dev: debug
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_user_id(name: str) -> str:
    cleaned = re.sub(r'[^\w\s-]', '', name)

    user_id = cleaned.strip().replace(' ', '_')

    user_id = user_id.lower()

    if not user_id:
        raise ValueError("Name must contain at least one alphanumeric character")

    logger.debug(f"Generated user_id '{user_id}' from name '{name}'")
    return user_id

@app.post("/api/upload-cv")
async def upload_cv(file: Annotated[UploadFile, File()]):
    """
    Upload and extract text from PDF CV
    """
    if not file.content_type == "application/pdf":
        logger.warning(f"Invalid file type upload: {file.content_type}"
                       f"(filename: {file.filename})"
                       )
        raise HTTPException(status_code=400, detail={"error": "invalid_file_type",
                            "message": "Only PDF files are allowed."})
    try:
        logger.info(f"Processing uploaded CV: {file.filename}")

        content = await file.read()
        pdf_file = io.BytesIO(content)
        text = extract_text_from_pdf(pdf_file)

        logger.info(f"Successfully extracted text from CV filename: {file.filename}")
        return {"status": "success", "cv_data": text}

    except ValueError as e:
        logger.warning(f"Invalid PDF file {file.filename}: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_pdf",
                "message": f"Can't proccess PDF: {str(e)}"
            }
        )

    except OSError as e:
        logger.error(f"File error {file.filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "file_error",
                "message": "Cannot read file. Please try again."
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error processing CV (filename: {file.filename}): {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={
            "error": "server_serror",
            "message": f"An unexpected error occured. Please try again later."})

    finally:
        await file.seek(0)

@app.post("/api/save-base-cv")
async def save_base_cv(cv_data: ParsedCV):
    user_id = validate_user_id(cv_data.name)
    logger.info(f"Attempting to save base CV for user: {user_id}")

    try:
        storage.save_base_cv(user_id, cv_data)
        logger.info(f"Successfully saved base CV for user: {user_id}")
        return {
            "status": "success",
            "message": "Base CV saved successfully",
            "data": {"user_id": user_id}
        }

    except StorageUnavailableError as e:
        logger.error(f"Storage failed for user {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "storage_failed",
                "message": "Could not save your CV. Please try again."
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error saving CV for {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "server_error",
                "message": "An unexpected error occurred"
            }
        )

@app.get("/api/get-base-cv")
async def get_base_cv(user_id: str):
    logger.debug(f"User {user_id} requested CV")
    user_id = validate_user_id(user_id)
    try:
        cv = storage.get_base_cv(user_id)
        if not cv:
            logger.warning(f"CV not found for user {user_id}")
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "cv_not_found",
                    "message": f"Couldn't find CV for user {user_id}. Please upload your CV again",
                    "action": "redirect_to_upload"
                }
            )
        logger.info(f"Succesfully loaded CV for user {user_id}")
        return {
            "success": True,
            "data": cv
        }

    except StorageUnavailableError as e:
        logger.error(f"Storage error for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "storage_error",
                "message": "Could not retrieve CV. Please try again."
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error fetching CV for {user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "server_error",
                "message": "An unexpected error occurred"
            }
        )

@app.post("/api/generate-pdf")
async def preview_pdf(user_id: str = "default"):
    logger.info(f"Generating PDF preview for user {user_id}")
    user_id = validate_user_id(user_id)
    try:
        cv = storage.get_base_cv(user_id)

        if not cv:
            logger.warning(f"CV not found for user {user_id}")
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "cv_not_found",
                    "message": f"Couldn't find CV for user {user_id}. Please upload your CV again",
                    "action": "redirect_to_upload"
                }
            )

        pdf_bytes = pdf_gen.generate_pdf(cv)
        filename = pdf_gen.generate_pdf_name(cv.name, cv.job_title)

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail={"error": "template_not_found", "message": "Template not found"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.post("/api/jobs/create")
async def create_job(job_application: JobApplication = Body(...)):
    """
    Recieving full JobApplication data from frontend after AI analysis
    """
    logger.info("Attempting to save job application")
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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(500, f"Failed to save: {str(e)}")

@app.get('/api/jobs/{job_id}')
async def view_job(
        user_id: str = Query(...),
        job_id: str = Path(...)):
    logger.info(f"Fetching job application: {job_id}")

    try:
        job_data = storage.get_job_application(user_id, job_id)

        if job_data is None:
            raise HTTPException(
                status_code=404,
                detail="No base data for job application found."
            )

        return job_data

    except HTTPException:
        raise

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
    logger.info(f"Fetching all jobs for user {user_id}")
    try:
        all_jobs_data = storage.get_all_jobs(user_id)

        if all_jobs_data is None:
            raise HTTPException(
                status_code=404,
                detail="No base data for job application found."
            )

        return all_jobs_data

    except HTTPException:
        raise

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

@app.post("/api/jobs/{job_id}/apply_changes")
async def apply_changes(
    job_id: str = Path(...),
    user_id: str = Query(...), #
    changes: List[dict] = Body(...)):
    logger.info(f"Attempting to apply changes in job {job_id}")
    try:
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

    except HTTPException:
        raise

@app.get("/api/jobs/{job_id}/download")
async def generate_and_download(
    user_id: str = Query(...),
    job_id: str = Path(...),
):
    try:
        job_application = storage.get_job_application(user_id, job_id)
        base_cv = storage.get_base_cv(user_id)

        if not job_application:
            # or not base_cv:
            raise HTTPException(status_code=404,
                                detail={
                                    "error": f"job_id_not_found",
                                    "message": f"We couldn't find your job application"
                                }
            )
        if not base_cv:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "base_cv_not_founf",
                    "message": "We couldn't find your CV"
                }
            )

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

    #sending httpexception to frontend
    except Exception as e:
        logger.error(f"PDF download failed for user {user_id}, job {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500,
                            detail={
                                "error": "failed_to_download_modified_PDF",
                                "message": "Failed to download PDF. Please try again."
                            })


@app.get("/")
def read_root():
    return {"message": "CV Optimizer API"}
