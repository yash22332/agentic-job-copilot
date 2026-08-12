import json

from fastapi.testclient import TestClient

from app.api.app import app
from app.api.routes import get_resume_service


class FakeLLMClient:
    """Fake LLM client used by the API test."""

    def generate(self, prompt: str) -> str:
        """Return deterministic resume analysis JSON."""
        return json.dumps(
            {
                "contact": {
                    "name": "API Test User",
                    "email": "api@test.com",
                    "phone": "1234567890",
                },
                "skills": [
                    {"name": "Python"},
                    {"name": "FastAPI"},
                ],
                "experience": [
                    {
                        "company": "Test Company",
                        "role": "Software Engineer",
                        "duration": "2 Years",
                    }
                ],
                "education": [
                    {"degree": "B.Tech"},
                ],
            }
        )


def get_fake_resume_service():
    """Provide a ResumeService using the fake LLM."""
    from app.services.resume_service import ResumeService

    return ResumeService(llm_client=FakeLLMClient())


app.dependency_overrides[get_resume_service] = get_fake_resume_service

client = TestClient(app)


def test_analyze_resume_api():
    """API should analyze an uploaded PDF without calling Gemini."""

    with open("data/sample_resume.pdf", "rb") as resume:
        response = client.post(
            "/resumes/analyze",
            files={
                "file": (
                    "sample_resume.pdf",
                    resume,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["contact"]["name"] == "API Test User"
    assert data["skills"][0]["name"] == "Python"