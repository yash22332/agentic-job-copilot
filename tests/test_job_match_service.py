import json

from app.models.job import JobDescription, JobMatch
from app.models.resume import (
    ContactInfo,
    Education,
    Experience,
    ResumeAnalysis,
    Skill,
)
from app.services.job_match_service import JobMatchService


class FakeLLMClient:
    """Fake LLM client for deterministic testing."""

    def generate(self, prompt: str) -> str:
        return json.dumps(
            {
                "match_score": 85,
                "matching_skills": [
                    "Python",
                    "FastAPI",
                    "SQL",
                ],
                "missing_skills": [
                    "Docker",
                ],
                "experience_match": "Strong",
                "recommendations": [
                    "Highlight FastAPI projects.",
                    "Add Docker experience if available.",
                ],
            }
        )


def test_job_match_service():
    """JobMatchService should return a validated JobMatch."""

    resume = ResumeAnalysis(
        contact=ContactInfo(name="Test User"),
        skills=[
            Skill(name="Python"),
            Skill(name="FastAPI"),
            Skill(name="SQL"),
        ],
        experience=[
            Experience(
                company="Test Company",
                role="Software Engineer",
                duration="2 Years",
            )
        ],
        education=[
            Education(degree="B.Tech")
        ],
    )

    job = JobDescription(
        title="Python Developer",
        company="Test Corp",
        description="Build Python APIs.",
        location="Remote",
        experience_required="2+ years",
        required_skills=[
            "Python",
            "FastAPI",
            "SQL",
            "Docker",
        ],
    )

    service = JobMatchService(
        llm_client=FakeLLMClient(),
    )

    result = service.analyze(
        resume=resume,
        job=job,
    )

    assert isinstance(result, JobMatch)
    assert result.match_score == 85
    assert "Python" in result.matching_skills
    assert "Docker" in result.missing_skills