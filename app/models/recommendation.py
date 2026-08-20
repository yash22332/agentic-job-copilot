from pydantic import BaseModel


class JobRecommendation(BaseModel):
    job_role: str
    experience: str
    skills_required: list[str]
    location: str
    salary: str
    relevance_score: int
    reasons: list[str]

class JobRecommendations(BaseModel):
    recommendations: list[JobRecommendation]