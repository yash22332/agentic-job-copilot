"""
Development-only fake LLM client.

Used to run the application without consuming real LLM API quota.
"""

import json


class FakeLLMClient:
    """Return deterministic responses for local development."""

    def generate(self, prompt: str) -> str:
        """Return deterministic responses for local development."""

        if "Job Ranking" in prompt:
            return json.dumps(
                {
                    "recommendations": [
                        {
                            "job_role": "Python AI Engineer",
                            "company": "Example AI Labs",
                            "description": (
                                "Build AI applications using Python, "
                                "FastAPI, LangGraph and LLM APIs."
                            ),
                            "experience": "2+ years",
                            "skills_required": [
                                "Python",
                                "FastAPI",
                                "LangGraph",
                            ],
                            "location": "Bangalore",
                            "salary": "₹10-15 LPA",
                            "url": (
                                "https://example.com/jobs/"
                                "python-ai-engineer"
                            ),
                            "relevance_score": 92,
                            "reasons": [
                                "Strong Python and FastAPI alignment."
                            ],
                        }
                    ]
                }
            )

        if "Job Match" in prompt:
            return json.dumps(
                {
                    "match_score": 85,
                    "matching_skills": [
                        "Python",
                        "FastAPI",
                        "LangGraph",
                    ],
                    "missing_skills": [
                        "Docker",
                    ],
                    "experience_match": "Strong",
                    "recommendations": [
                        "Highlight Python and FastAPI experience.",
                        "Add Docker experience if available.",
                    ],
                }
            )

        return json.dumps(
            {
                "contact": {
                    "name": "Development User",
                    "email": "dev@example.com",
                    "phone": "0000000000",
                },
                "skills": [
                    {"name": "Python"},
                    {"name": "FastAPI"},
                    {"name": "LangGraph"},
                ],
                "experience": [
                    {
                        "company": "Development Company",
                        "role": "Software Engineer",
                        "duration": "2 Years",
                    }
                ],
                "education": [
                    {"degree": "B.Tech"},
                ],
            }
        )