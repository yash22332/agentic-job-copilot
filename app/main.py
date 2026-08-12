    # """
    # Application entry point.

    # This file is responsible for starting the application.
    # """

    # from app.llm import LLMClient
    # from app.config import get_settings


    # def main() -> None:
    #     """Run a simple connectivity test with Gemini."""

    #     settings = get_settings()

    #     print("=" * 50)
    #     print("Agentic Job Copilot")
    #     print("=" * 50)
    #     print(f"Using model: {settings.llm_model}")
    #     print()

    #     client = LLMClient()

    #     response = client.generate("Say hello in one sentence.")

    #     print("Gemini Response:")
    #     print(response)


    # if __name__ == "__main__":
    #     main()



"""
Application entry point.
"""

from app.llm import LLMClient
from app.services.resume_service import ResumeService

def main(llm_client: LLMClient | None = None) -> None:
    """Run the resume analysis application."""

    if llm_client is None:
        llm_client = LLMClient()

    resume_service = ResumeService(
    llm_client=llm_client,
    )

    result = resume_service.analyze(
        "data/sample_resume.pdf"
    )

    print("Resume Analysis:")
    print(result)


if __name__ == "__main__":
    main()