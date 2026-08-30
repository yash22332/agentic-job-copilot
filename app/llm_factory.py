"""
Create the appropriate LLM client for the application.
"""

from app.config import get_settings
from app.dev_llm import FakeLLMClient
from app.llm import LLMClient


def create_llm_client():
    """Create an LLM client based on application settings."""

    settings = get_settings()

    if settings.llm_mode.lower() == "fake":
        return FakeLLMClient()

    return LLMClient()