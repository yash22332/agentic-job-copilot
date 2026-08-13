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

    def generate(self, prompt: str) -> str:
        return """
        {
            "match_score": 90,
            "matching_skills": ["Python", "FastAPI"],
            "missing_skills": ["Docker"],
            "experience_match": "Strong",
            "recommendations": ["Highlight FastAPI experience."]
        }
        """


def test_job_match_workflow():
    """Workflow should produce a JobMatch in state."""

    resume = ResumeAnalysis(
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

    job = JobDescription(
        title="Python Developer",
        company="Test Corp",
        description="Build Python APIs.",
        required_skills=["Python", "FastAPI", "Docker"],
    )

    graph = build_job_match_graph(
        llm_client=FakeLLMClient(),
    )

    result = graph.invoke(
        {
            "resume": resume,
            "job": job,
        }
    )

    assert result["match"].match_score == 90
    assert "Docker" in result["match"].missing_skills