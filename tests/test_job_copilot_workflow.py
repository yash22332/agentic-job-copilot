import asyncio

from app.models.resume import (
    ContactInfo,
    Education,
    Experience,
    ResumeAnalysis,
    Skill,
)
from app.workflows.job_copilot_workflow import (
    build_job_copilot_graph,
)


class FakeLLMClient:
    """Fake LLM client for orchestrator testing."""

    def generate(self, prompt: str) -> str:
        """Return deterministic job-ranking JSON."""

        return """
{
    "recommendations": [
        {
            "job_role": "Python AI Engineer",
            "company": "Example AI Labs",
            "description": "Build AI applications using Python, FastAPI and LangGraph.",
            "experience": "2+ years",
            "skills_required": [
                "Python",
                "FastAPI",
                "LangGraph"
            ],
            "location": "Bangalore",
            "salary": "₹10-15 LPA",
            "url": "https://example.com/jobs/python-ai-engineer",
            "relevance_score": 92,
            "reasons": [
                "Strong Python and FastAPI alignment."
            ]
        }
    ]
}
"""


def test_job_copilot_workflow() -> None:
    """Job Copilot should search and rank jobs."""

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

    graph = build_job_copilot_graph(
        llm_client=FakeLLMClient(),
    )

    result = asyncio.run(
    graph.ainvoke(
        {
            "resume": resume,
            "query": "Python",
            "location": "Bangalore",
        }
    )
)

    assert result["jobs"]
    assert result["recommendations"].recommendations

    recommendation = (
        result["recommendations"]
        .recommendations[0]
    )

    assert recommendation.job_role == "Python AI Engineer"
    assert recommendation.relevance_score == 92