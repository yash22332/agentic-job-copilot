"""
LLM client for communicating with Gemini.

This module is the ONLY place in the application that talks to an LLM.
Other modules should never import the Gemini SDK directly.
"""

from google import genai

from app.config import get_settings


class LLMClient:
    """
    Client responsible for communicating with the configured LLM.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._client = genai.Client(
            api_key=settings.llm_api_key
        )

        self._model = settings.llm_model

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        """

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
    
        return response.text