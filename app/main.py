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

import json

from app.llm import LLMClient
from app.prompt_loader import load_prompt
from app.prompt_builder import build_prompt
from app.resume_parser import parse_resume
from app.models.resume import ResumeAnalysis

def main():

    resume = parse_resume("data/sample_resume.txt")

    template = load_prompt("resume_analysis.md")

    prompt = build_prompt(
        template,
        resume_text=resume
    )

    client = LLMClient()

    response = client.generate(prompt)

    print("Raw Gemini Response:")
    print(response)

    print("\nTrying to parse JSON...\n")

    data = json.loads(response)
    
    resume_analysis = ResumeAnalysis.model_validate(data)

    print("\nValidated Resume Analysis:")
    print(resume_analysis)


if __name__ == "__main__":
    main()