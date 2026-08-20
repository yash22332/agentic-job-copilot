# from app.workflows.job_search_workflow import build_job_search_graph


# def test_job_search_workflow():
#     """Job search workflow should retrieve jobs through MCP."""

#     graph = build_job_search_graph()

#     result = graph.invoke(
#         {
#             "query": "Python",
#             "location": "Bangalore",
#         }
#     )

#     assert "jobs" in result
#     assert result["jobs"]

#     first_job = result["jobs"][0]

#     assert "title" in first_job
#     assert "company" in first_job
#     assert "location" in first_job
#     assert "url" in first_job

import json

from app.workflows.job_search_workflow import build_job_search_graph
from app.models.resume import(
    ContactInfo,
    Education,
    Experience,
    ResumeAnalysis,
    Skill,
)


class FakeLLMClient:
    """Fake LLM client for job-ranking tests."""

    def generate(self, prompt: str) -> str:
        """Return deterministic ranking JSON."""

        return json.dumps(
            {
                "recommendations": [
                    {
                        "job_role": "Python AI Engineer",
                        "experience": "2+ years",
                        "skills_required": [
                            "Python",
                            "FastAPI",
                            "LangGraph",
                        ],
                        "location": "Bangalore",
                        "salary": "₹10-15 LPA",
                        "relevance_score": 92,
                        "reasons": [
                            "Strong Python and FastAPI alignment."
                        ],
                    }
                ]
            }
        )


def test_job_search_workflow():
    """Job search workflow should retrieve and rank jobs."""

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


    graph = build_job_search_graph(
        llm_client=FakeLLMClient(),
    )

    result = graph.invoke(
        {
            "query": "Python",
            "location": "Bangalore",
            "resume": resume,
        }
    )

    assert result["jobs"]
    assert result["recommendations"].recommendations
    assert (
        result["recommendations"]
        .recommendations[0]
        .relevance_score
        == 92
    )