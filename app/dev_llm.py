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
            jobs_text = prompt.split(
                "Jobs:",
                1,
            )[1].strip()

            jobs = json.loads(jobs_text)

            recommendations = []

            for job in jobs:
                recommendations.append(
                    {
                        "job_role": job.get("title", ""),
                        "company": job.get("company", ""),
                        "description": job.get(
                            "description",
                            "",
                        ),
                        "experience": "",
                        "skills_required": [],
                        "location": job.get(
                            "location",
                            "",
                        ),
                        "salary": job.get(
                            "salary",
                            "",
                        ),
                        "url": job.get("url", ""),
                        "relevance_score": 80,
                        "reasons": [
                            "Job retrieved from the live job source."
                        ],
                    }
                )

            recommendations.sort(
                key=lambda job: job["relevance_score"],
                reverse=True,
            )

            return json.dumps(
                {
                    "recommendations": recommendations,
                }
            )

        if "Job Match Analysis" in prompt:
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