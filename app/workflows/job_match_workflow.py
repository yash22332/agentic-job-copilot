from typing import TypedDict

from app.models.job import JobDescription, JobMatch
from app.models.resume import ResumeAnalysis


class JobMatchState(TypedDict, total=False):
    resume: ResumeAnalysis
    job: JobDescription
    match: JobMatch

from app.llm import LLMClient
from app.services.job_match_service import JobMatchService


def create_job_match_node(llm_client: LLMClient):
    """Create a LangGraph node for job matching."""

    service = JobMatchService(llm_client=llm_client)

    def job_match_node(state: JobMatchState) -> dict:
        """Match the resume against the job description."""

        match = service.analyze(
            resume=state["resume"],
            job=state["job"],
        )

        return {
            "match": match,
        }

    return job_match_node

from langgraph.graph import END, START, StateGraph

def build_job_match_graph(llm_client: LLMClient):
    """Build and compile the job matching workflow."""

    graph = StateGraph(JobMatchState)

    job_match_node = create_job_match_node(llm_client)

    graph.add_node("job_match", job_match_node)

    graph.add_edge(START, "job_match")
    graph.add_edge("job_match", END)

    return graph.compile()