from pydantic import BaseModel
from typing import Optional, List

class Project(BaseModel):
    title: str
    tools: Optional[str] = None
    description: List[str]
    link: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    date: str
    description: List[str]

class Education(BaseModel):
    degree: str
    field: str
    school_name: str
    date: str

class ParsedCV(BaseModel):
    name: str
    email: str
    location: str
    phone: str

    job_title: str
    bio: str

    skills: List[str]
    languages: List[str]

    projects: Optional[List[Project]] = None
    experience: List[Experience]
    education: List[Education]

# class JobRequirements(BaseModel):

# class Suggestion(BaseModel):