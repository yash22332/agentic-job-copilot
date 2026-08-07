"""
Application entry point.

This file is responsible for starting the application.
"""

from app.llm import LLMClient
from app.config import get_settings


def main() -> None:
    """Run a simple connectivity test with Gemini."""

    settings = get_settings()

    print("=" * 50)
    print("Agentic Job Copilot")
    print("=" * 50)
    print(f"Using model: {settings.llm_model}")
    print()

    client = LLMClient()

    response = client.generate("Say hello in one sentence.")

    print("Gemini Response:")
    print(response)


if __name__ == "__main__":
    main()