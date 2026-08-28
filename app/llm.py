"""
LLM client for communicating with Gemini.

This module is the ONLY place in the application that talks to an LLM.

Other modules should never import the Gemini SDK directly.
"""

from google import genai
from google.genai import errors

from app.config import get_settings


class LLMClient:
    """Client responsible for communicating with the configured LLM."""

    def __init__(self) -> None:
        settings = get_settings()

        self._client = genai.Client(
            api_key=settings.llm_api_key
        )
        self._model = settings.llm_model

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the generated text.

        Raises:
            RuntimeError: If Gemini reports a quota or service error.
        """

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
            )

        except errors.ClientError as exc:
            if exc.code == 429:
                raise RuntimeError(
                    "Gemini quota exceeded. "
                    "Switch to fake mode or wait for the quota to reset."
                ) from exc

            raise RuntimeError(
                f"Gemini client error: {exc}"
            ) from exc

        except errors.ServerError as exc:
            raise RuntimeError(
                f"Gemini service unavailable: {exc}"
            ) from exc

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text