"""
Application configuration.

This module is responsible for loading configuration from the environment.
No other module should directly access environment variables.
"""

from dataclasses import dataclass

import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_api_key: str
    llm_model: str


def get_settings() -> Settings:
    return Settings(
        llm_api_key=os.getenv("GEMINI_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "gemini-flash-latest"),
    )