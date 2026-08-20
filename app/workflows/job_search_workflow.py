import asyncio
from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from app.mcp.client import search_jobs
from app.llm import LLMClient
from app.models.recommendation import JobRecommendations
from app.models.resume import ResumeAnalysis
from app.services.job_ranking_service import JobRankingService

class JobSearchState(TypedDict, total=False):
    query: str
    location: str
    resume: ResumeAnalysis
    jobs: list[dict[str, str]]
    recommendations: JobRecommendations

def search_jobs_node(
    state: JobSearchState,
) -> dict[str, list[dict[str, str]]]:
    """Search for jobs through the MCP server."""

    jobs = asyncio.run(
        search_jobs(
            query=state["query"],
            location=state.get("location", ""),
        )
    )

    return {
        "jobs": jobs,
    }

def create_job_ranking_node(llm_client: LLMClient):
    """Create the job-ranking LangGraph node."""

    service = JobRankingService(
        llm_client=llm_client,
    )

    def job_ranking_node(
        state: JobSearchState,
    ) -> dict[str, JobRecommendations]:
        """Rank jobs using the candidate's resume."""

        recommendations = service.rank(
            resume=state["resume"],
            jobs=state["jobs"],
        )

        return {
            "recommendations": recommendations,
        }

    return job_ranking_node

def build_job_search_graph(llm_client: LLMClient):
    """Build and compile the job search workflow."""
    rank_node = create_job_ranking_node(llm_client)
    graph = StateGraph(JobSearchState)

    graph.add_node("search_jobs", search_jobs_node)
    graph.add_node("rank_jobs", rank_node)

    graph.add_edge(START, "search_jobs")
    graph.add_edge("search_jobs", "rank_jobs")
    graph.add_edge("rank_jobs", END)
    
    return graph.compile()

