# """
# HTTP routes for the Agentic Job Copilot.
# """

# from pathlib import Path
# from uuid import uuid4

# from fastapi import APIRouter, File, UploadFile

# from app.llm import LLMClient
# from app.services.resume_service import ResumeService

# router = APIRouter()

# UPLOAD_DIR = Path("data/uploads")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# @router.get("/health")
# def health_check() -> dict[str, str]:
#     """Return a simple health status."""
#     return {"status": "ok"}


# @router.post("/resumes/analyze")
# async def analyze_resume(file: UploadFile = File(...)):
#     """Analyze an uploaded resume PDF."""

#     file_extension = Path(file.filename or "").suffix.lower()

#     if file_extension != ".pdf":
#         return {"error": "Only PDF resumes are supported."}

#     file_path = UPLOAD_DIR / f"{uuid4()}{file_extension}"

#     contents = await file.read()
#     file_path.write_bytes(contents)

#     llm_client = LLMClient()
#     resume_service = ResumeService(llm_client=llm_client)

#     result = resume_service.analyze(str(file_path))

#     return result
"""
HTTP routes for the Agentic Job Copilot.
"""
import json

from fastapi import Form, HTTPException
from pathlib import Path
from uuid import uuid4
from app.models.job import JobDescription
from app.services.job_match_service import JobMatchService

from fastapi import APIRouter, Depends, File, UploadFile

from app.llm import LLMClient
from app.services.resume_service import ResumeService

from fastapi import Form

from app.models.resume import ResumeAnalysis
from app.workflows.job_search_workflow import build_job_search_graph
from app.llm_factory import create_llm_client
router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# def get_resume_service() -> ResumeService:
#     """Create the resume service used by API routes."""
#     return ResumeService(llm_client=LLMClient())

def get_resume_service() -> ResumeService:
    """Create the resume service used by API routes."""
    return ResumeService(llm_client=create_llm_client())

@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health status."""
    return {"status": "ok"}


@router.post("/resumes/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Analyze an uploaded resume PDF."""

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension != ".pdf":
        return {"error": "Only PDF resumes are supported."}

    file_path = UPLOAD_DIR / f"{uuid4()}{file_extension}"

    contents = await file.read()
    file_path.write_bytes(contents)

    result = resume_service.analyze(str(file_path))

    return result

# def get_job_match_service() -> JobMatchService:
#     """Create the job matching service used by API routes."""
#     return JobMatchService(llm_client=LLMClient())

def get_job_match_service() -> JobMatchService:
    """Create the job matching service used by API routes."""
    return JobMatchService(llm_client=create_llm_client())

@router.post("/jobs/match")
async def match_job(
    file: UploadFile = File(...),
    job: str = Form(...),
    resume_service: ResumeService = Depends(get_resume_service),
    job_match_service: JobMatchService = Depends(get_job_match_service),
):
    """Match an uploaded resume against a job description."""

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    try:
        job_data = json.loads(job)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Job must be valid JSON.",
        ) from exc

    try:
        job_description = JobDescription.model_validate(job_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid job description: {exc}",
        ) from exc

    file_path = UPLOAD_DIR / f"{uuid4()}{file_extension}"

    contents = await file.read()
    file_path.write_bytes(contents)

    resume = resume_service.analyze(str(file_path))

   
    result = job_match_service.analyze(
        resume=resume,
        job=job_description,
    )

    return result

@router.post("/jobs/search")
async def search_jobs_route(
    file: UploadFile = File(...),
    query: str = Form(...),
    location: str = Form(""),
    resume_service: ResumeService = Depends(get_resume_service),
):
    """Search and rank jobs against an uploaded resume."""

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    file_path = UPLOAD_DIR / f"{uuid4()}{file_extension}"

    contents = await file.read()
    file_path.write_bytes(contents)

    resume = resume_service.analyze(str(file_path))

    # Use the same shared LLM client as the resume service.
    # graph = build_job_search_graph(
    #     llm_client = resume_service._llm_client,
    # )

    graph = build_job_search_graph(
    llm_client=create_llm_client(),
)

    result = await graph.ainvoke(
        {
            "query": query,
            "location": location,
            "resume": resume,
        }
    )

    return result["recommendations"]