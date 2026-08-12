from pydantic import BaseModel


class ContactInfo(BaseModel):
    name: str
    email: str = ""
    phone: str = ""


class Skill(BaseModel):
    name: str


class Experience(BaseModel):
    company: str
    role: str
    duration: str


class Education(BaseModel):
    degree: str


class ResumeAnalysis(BaseModel):
    contact: ContactInfo
    skills: list[Skill]
    experience: list[Experience]
    education: list[Education]