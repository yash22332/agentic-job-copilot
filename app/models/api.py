from pydantic import BaseModel

from app.models.job import JobDescription


class JobMatchRequest(BaseModel):
    job: JobDescription