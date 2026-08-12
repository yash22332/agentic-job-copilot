"""
Resume analysis service.

Coordinates resume parsing, prompt construction, LLM generation,
and structured response validation.
"""

import json

from app.llm import LLMClient
from app.models.resume import ResumeAnalysis
from app.prompt_builder import build_prompt
from app.prompt_loader import load_prompt
from app.resume_parser import parse_resume


class ResumeService:
    """Service responsible for analyzing resumes."""

    def __init__(self, llm_client: LLMClient) -> None:
        """
        Initialize the resume service.

        Args:
            llm_client: Shared LLM client used for AI operations.
        """
        self._llm_client = llm_client

    def analyze(self, file_path: str) -> ResumeAnalysis:
        """
        Analyze a resume and return validated structured data.

        Args:
        file_path: Path to the resume file.

        Returns:
        Validated ResumeAnalysis object.
        """

        resume_text = parse_resume(file_path)

        template = load_prompt("resume_analysis.md")

        prompt = build_prompt(
        template,
        resume_text=resume_text,
        )

        response = self._llm_client.generate(prompt)

        data = json.loads(response)

        return ResumeAnalysis.model_validate(data)
    
        