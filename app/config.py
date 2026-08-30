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
    llm_provider: str = "gemini"
    llm_api_key: str = ""
    llm_model: str = "gemini-3.6-flash"
    llm_mode: str = "fake"
    data_directory: str = "data"
    max_file_size_mb: int = 10


def get_settings() -> Settings:
    return Settings(
        llm_api_key=os.getenv("GEMINI_API_KEY", ""),
        llm_model=os.getenv("LLM_MODEL", "gemini-3.6-flash"),
        llm_mode=os.getenv("LLM_MODE", "fake"),
    )