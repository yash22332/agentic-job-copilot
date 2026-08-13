from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    title: str
    company: str
    description: str
    location: str = ""
    experience_required: str = ""
    required_skills: list[str] = Field(default_factory=list)

class JobMatch(BaseModel):
    match_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    experience_match: str
    recommendations: list[str]