from pydantic import BaseModel


class JobRecommendation(BaseModel):
    job_role: str
    company: str
    description: str
    experience: str
    skills_required: list[str]
    location: str
    salary: str
    url: str
    relevance_score: int
    reasons: list[str]


class JobRecommendations(BaseModel):
    recommendations: list[JobRecommendation]