"""
Job ranking service.
"""

import json

from app.llm import LLMClient
from app.models.recommendation import JobRecommendations
from app.models.resume import ResumeAnalysis
from app.prompt_builder import build_prompt
from app.prompt_loader import load_prompt


class JobRankingService:
    """Rank retrieved jobs for a candidate."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm_client = llm_client

    def rank(
        self,
        resume: ResumeAnalysis,
        jobs: list[dict[str, str]],
    ) -> JobRecommendations:
        """Rank jobs based on the candidate's resume."""

        template = load_prompt("job_ranking.md")

        prompt = build_prompt(
            template,
            resume=json.dumps(
                resume.model_dump(),
                indent=2,
            ),
            jobs=json.dumps(
                jobs,
                indent=2,
            ),
        )

        response = self._llm_client.generate(prompt)

        print("\n--- RAW JOB RANKING RESPONSE ---")
        response = self._llm_client.generate(prompt)
        data = json.loads(response)

        return JobRecommendations.model_validate(data)