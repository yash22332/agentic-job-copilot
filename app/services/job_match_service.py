"""
Job matching service.

Compares a candidate resume against a job description
and returns a validated JobMatch result.
"""

import json

from app.llm import LLMClient
from app.models.job import JobDescription, JobMatch
from app.models.resume import ResumeAnalysis
from app.prompt_builder import build_prompt
from app.prompt_loader import load_prompt


class JobMatchService:
    """Service responsible for matching a resume to a job."""

    def __init__(self, llm_client: LLMClient) -> None:
        """Initialize the service with a shared LLM client."""
        self._llm_client = llm_client

    def analyze(
        self,
        resume: ResumeAnalysis,
        job: JobDescription,
    ) -> JobMatch:
        """
        Analyze how well a resume matches a job description.

        Args:
            resume: Structured candidate resume.
            job: Structured job description.

        Returns:
            A validated JobMatch result.
        """

        template = load_prompt("job_match.md")

        prompt = build_prompt(
            template,
            resume=json.dumps(resume.model_dump(), indent=2),
            job=json.dumps(job.model_dump(), indent=2),
        )

        response = self._llm_client.generate(prompt)

        data = json.loads(response)

        return JobMatch.model_validate(data)