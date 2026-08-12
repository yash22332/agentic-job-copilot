import json

from app.models.resume import ResumeAnalysis
from app.services.resume_service import ResumeService


class FakeLLMClient:
    """Fake LLM client used for testing."""

    def generate(self, prompt: str) -> str:
        """Return deterministic resume analysis JSON."""

        return json.dumps(
            {
                "contact": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "phone": "1234567890",
                },
                "skills": [
                    {"name": "Python"},
                    {"name": "SQL"},
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


def test_resume_service_returns_resume_analysis() -> None:
    """ResumeService should return a validated ResumeAnalysis."""

    service = ResumeService(
        llm_client=FakeLLMClient(),
    )

    result = service.analyze("data/sample_resume.txt")

    assert isinstance(result, ResumeAnalysis)
    assert result.contact.name == "Test User"
    assert result.skills[0].name == "Python"
    assert result.experience[0].company == "Test Company"