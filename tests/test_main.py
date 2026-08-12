import json

from app.main import main


class FakeLLMClient:
    """Fake LLM client for application-level tests."""

    def generate(self, prompt: str) -> str:
        """Return deterministic resume analysis data."""

        return json.dumps(
            {
                "contact": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "phone": "1234567890",
                },
                "skills": [
                    {"name": "Python"},
                ],
                "experience": [
                    {
                        "company": "Test Company",
                        "role": "Software Engineer",
                        "duration": "2 Years",
                    }
                ],
                "education": [
                    {"degree": "Bachelor of Engineering"}
                ],
            }
        )


def test_main_runs_without_error(capsys):
    """The application should run without calling Gemini."""

    main(llm_client=FakeLLMClient())

    captured = capsys.readouterr()

    assert "Resume Analysis:" in captured.out
    assert "Test User" in captured.out