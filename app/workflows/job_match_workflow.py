from typing import TypedDict
from app.models.job import JobDescription, JobMatch
from app.models.resume import ResumeAnalysis
from langgraph.graph import END, START, StateGraph
from app.llm import LLMClient
from app.services.job_match_service import JobMatchService


class JobMatchState(TypedDict, total=False):
    resume: ResumeAnalysis
    job: JobDescription
    match: JobMatch
    match_category: str




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

def evaluate_match_node(
    state: JobMatchState,
    ) -> dict[str, str]:
        """Classify the job match based on its score."""
        
        match_score = state["match"].match_score

        if match_score >= 70:
            return {"match_category": "strong_match"}
        
        return {"match_category": "needs_improvement"}

def route_match(
    state: JobMatchState,
) -> str:
    """Choose the next graph node based on match category."""

    return state["match_category"]

def strong_match_node(
    state: JobMatchState,
) -> dict[str, str]:
    """Handle strong job matches."""

    return {
        "match_category": "strong_match",
    }


def needs_improvement_node(
    state: JobMatchState,
) -> dict[str, str]:
    """Handle weaker job matches."""

    return {
        "match_category": "needs_improvement",
    }

# def build_job_match_graph(llm_client: LLMClient):
#     """Build and compile the job matching workflow."""

#     graph = StateGraph(JobMatchState)

#     job_match_node = create_job_match_node(llm_client)

#     graph.add_node("job_match", job_match_node)

#     graph.add_edge(START, "job_match")
#     graph.add_edge("job_match", END)

#     return graph.compile() 


def build_job_match_graph(llm_client: LLMClient):
    """Build and compile the job matching workflow."""

    graph = StateGraph(JobMatchState)

    job_match_node = create_job_match_node(llm_client)

    graph.add_node("job_match", job_match_node)
    graph.add_node("evaluate_match", evaluate_match_node)
    graph.add_node("strong_match", strong_match_node)
    graph.add_node(
        "needs_improvement",
        needs_improvement_node,
    )

    graph.add_edge(START, "job_match")
    graph.add_edge("job_match", "evaluate_match")

    graph.add_conditional_edges(
        "evaluate_match",
        route_match,
        {
            "strong_match": "strong_match",
            "needs_improvement": "needs_improvement",
        },
    )

    graph.add_edge("strong_match", END)
    graph.add_edge("needs_improvement", END)

    return graph.compile()