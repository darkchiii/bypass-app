from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime

# CV models
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

# Job Application Models
class JobRequirements(BaseModel):
    job_title: str
    company: str
    key_skills: List[str]
    important_keywords: List[str]
    responsibilities: List[str]
    company_values: List[str]
    tone: str

class Suggestion(BaseModel):
    type: Literal["rewrite", "reorder", "update_field", "add_keyword", "emphasize"]
    section: Literal["job_title", "bio", "skills", "experience", "projects", "education", "languages"]
    target: Optional[str]  # Dokładna lokalizacja (np. "experience[0].description[1]")
    current_value: str  # Co jest teraz
    suggested_value: str  # Co AI proponuje
    reason: str  # Dlaczego ta zmiana
    status: Literal["pending", "accepted", "rejected", "modified"]
    final_value: Optional[str]  # Co user ostatecznie wpisał (jeśli zmodyfikował)

class JobApplication(BaseModel):
    job_id: str
    user_id: str
    job_requirements: JobRequirements
    suggestions: List[Suggestion]
    status: Literal["pending", "ready", "downloaded"]
    analysis_model: Literal["quick", "full"] = "full"
    # created_at: datetime
