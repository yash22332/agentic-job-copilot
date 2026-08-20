import json

from app.models.job import JobDescription
from app.models.resume import (
    ContactInfo,
    Education,
    Experience,
    ResumeAnalysis,
    Skill,
)
from app.workflows.job_match_workflow import build_job_match_graph



class FakeLLMClient:
    """Deterministic LLM client for workflow testing."""

    def __init__(self, match_score: int) -> None:
        self.match_score = match_score

    def generate(self, prompt: str) -> str:
        """Return deterministic job-match JSON."""

        if self.match_score >= 70:
            return json.dumps(
                {
                    "match_score": 90,
                    "matching_skills": [
                        "Python",
                        "FastAPI",
                    ],
                    "missing_skills": [
                        "Docker",
                    ],
                    "experience_match": "Strong",
                    "recommendations": [
                        "Highlight FastAPI experience."
                    ],
                }
            )

        return json.dumps(
            {
                "match_score": 50,
                "matching_skills": [
                    "Python",
                ],
                "missing_skills": [
                    "FastAPI",
                    "Docker",
                ],
                "experience_match": "Weak",
                "recommendations": [
                    "Gain more API development experience."
                ],
            }
        )


def create_test_resume() -> ResumeAnalysis:
    """Create a reusable test resume."""

    return ResumeAnalysis(
        contact=ContactInfo(name="Test User"),
        skills=[
            Skill(name="Python"),
            Skill(name="FastAPI"),
        ],
        experience=[
            Experience(
                company="Test Company",
                role="Software Engineer",
                duration="2 Years",
            )
        ],
        education=[
            Education(degree="B.Tech"),
        ],
    )


def create_test_job() -> JobDescription:
    """Create a reusable test job."""

    return JobDescription(
        title="Python Developer",
        company="Test Corp",
        description="Build Python APIs.",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
        ],
    )


def test_strong_job_match() -> None:
    """A high match score should route to strong_match."""

    graph = build_job_match_graph(
        llm_client=FakeLLMClient(match_score=90),
    )

    result = graph.invoke(
        {
            "resume": create_test_resume(),
            "job": create_test_job(),
        }
    )

    assert result["match"].match_score == 90
    assert result["match_category"] == "strong_match"
    assert "Docker" in result["match"].missing_skills


def test_weak_job_match() -> None:
    """A low match score should route to needs_improvement."""

    graph = build_job_match_graph(
        llm_client=FakeLLMClient(match_score=50),
    )

    result = graph.invoke(
        {
            "resume": create_test_resume(),
            "job": create_test_job(),
        }
    )

    assert result["match"].match_score == 50
    assert result["match_category"] == "needs_improvement"
    assert "Docker" in result["match"].missing_skills

