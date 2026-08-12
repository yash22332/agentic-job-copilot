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

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile

from app.llm import LLMClient
from app.services.resume_service import ResumeService

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_resume_service() -> ResumeService:
    """Create the resume service used by API routes."""
    return ResumeService(llm_client=LLMClient())


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