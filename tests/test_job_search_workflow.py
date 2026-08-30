import json
import asyncio
from app.workflows.job_search_workflow import build_job_search_graph
from app.models.resume import(
    ContactInfo,
    Education,
    Experience,
    ResumeAnalysis,
    Skill,
)

def test_job_search_workflow():
    """Job search workflow should retrieve and rank jobs."""

    graph = build_job_search_graph()

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

    result = asyncio.run(
    graph.ainvoke(
            {
                "query": "Python",
                "location": "Bangalore",
                "resume": resume,
            }
        )
    )

    assert result["jobs"]

    job = result["jobs"][0]

    assert job["title"]
    assert job["company"]
    assert job["location"]
    assert job["description"]
    assert job["url"]