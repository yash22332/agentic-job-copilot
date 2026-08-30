from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.mcp.client import search_jobs


class JobSearchState(TypedDict, total=False):
    query: str
    location: str
    jobs: list[dict[str, str]]


async def search_jobs_node(
    state: JobSearchState,
) -> dict[str, list[dict[str, str]]]:
    """Search real jobs through the MCP server."""

    jobs = await search_jobs(
        query=state["query"],
        location=state.get("location", ""),
    )

    return {
        "jobs": jobs,
    }


def build_job_search_graph():
    """Build and compile the job-search workflow."""

    graph = StateGraph(JobSearchState)

    graph.add_node(
        "search_jobs",
        search_jobs_node,
    )

    graph.add_edge(START, "search_jobs")
    graph.add_edge("search_jobs", END)

    return graph.compile()