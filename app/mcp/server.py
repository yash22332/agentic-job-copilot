"""
MCP server for Agentic Job Copilot.
"""

from mcp.server import MCPServer


mcp = MCPServer("Job Copilot Tools")


JOBS = [
    {
        "title": "Python AI Engineer",
        "company": "Example AI Labs",
        "location": "Bangalore",
        "description": (
            "Build AI applications using Python, FastAPI, "
            "LangGraph and LLM APIs."
        ),
        "url": "https://example.com/jobs/python-ai-engineer",
        "salary": "₹10-15 LPA",
    },
    {
        "title": "GenAI Engineer",
        "company": "Cloud AI Systems",
        "location": "Hyderabad",
        "description": (
            "Develop RAG pipelines, agentic workflows and "
            "MCP integrations."
        ),
        "url": "https://example.com/jobs/genai-engineer",
        "salary": "₹12-18 LPA",
    },
    {
        "title": "Backend Python Developer",
        "company": "Tech Solutions",
        "location": "Pune",
        "description": (
            "Develop REST APIs using Python, FastAPI and PostgreSQL."
        ),
        "url": "https://example.com/jobs/python-backend",
        "salary": "₹8-12 LPA",
    },
]


@mcp.tool()
def search_jobs(
    query: str,
    location: str = "",
) -> list[dict[str, str]]:
    """
    Search available jobs by keyword and location.

    The tool returns only the fields required by Job Copilot.
    """

    query_lower = query.lower()
    location_lower = location.lower()

    results = []

    for job in JOBS:
        matches_query = (
            query_lower in job["title"].lower()
            or query_lower in job["description"].lower()
        )

        matches_location = (
            not location_lower
            or location_lower in job["location"].lower()
        )

        if matches_query and matches_location:
            results.append(job)

    return results


if __name__ == "__main__":
    mcp.run()