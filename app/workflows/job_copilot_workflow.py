import asyncio
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.llm import LLMClient
from app.models.recommendation import JobRecommendations
from app.models.resume import ResumeAnalysis
from app.workflows.job_search_workflow import build_job_search_graph


class JobCopilotState(TypedDict, total=False):
    resume: ResumeAnalysis
    query: str
    location: str
    jobs: list[dict[str, str]]
    recommendations: JobRecommendations


async def search_jobs_node(
    state: JobCopilotState,
    llm_client: LLMClient,
) -> dict:
    """Run the existing job-search workflow."""

    graph = build_job_search_graph(
        llm_client=llm_client,
    )

    result = await graph.ainvoke(
        {
            "query": state["query"],
            "location": state.get("location", ""),
            "resume": state["resume"],
        }
    )

    return {
        "jobs": result["jobs"],
        "recommendations": result["recommendations"],
    }


def create_copilot_search_node(llm_client: LLMClient):
    """Create the Job Copilot search node."""

    async def copilot_search_node(
        state: JobCopilotState,
    ) -> dict:
        return await search_jobs_node(
            state,
            llm_client,
        )

    return copilot_search_node


def build_job_copilot_graph(llm_client: LLMClient):
    """Build and compile the Job Copilot graph."""

    graph = StateGraph(JobCopilotState)

    graph.add_node(
        "search_jobs",
        create_copilot_search_node(llm_client),
    )

    graph.add_edge(START, "search_jobs")
    graph.add_edge("search_jobs", END)

    return graph.compile()