from pydantic import BaseModel, EmailStr, Field, field_validator
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
    email: EmailStr
    location: str
    phone: str

    job_title: str
    bio: str

    skills: List[str]
    languages: List[str]

    projects: Optional[List[Project]] = None
    experience: List[Experience]
    education: List[Education]

@field_validator('phone')
def validate_phone(cls, v):
    """Sprawdź czy phone ma cyfry"""
    if not any(char.isdigit() for char in v):
        raise ValueError('Phone must contain at least one digit')
    return v

@field_validator('name')
def validate_name(cls, v):
    """Sprawdź czy name nie jest pusty po strip"""
    if not v.strip():
        raise ValueError('Name cannot be empty')
    return v.strip()

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
    type: Literal["rewrite", "reorder", "update_field"]
    section: Literal["job_title", "bio", "skills", "experience", "projects", "education", "languages"]

    # Dla zagniezdzonych zmian
    target_item_index: Optional[int] = None
    target_field: Optional[str] = None
    target_field_index: Optional[int] = None

    current_value: str  # Co jest teraz
    suggested_value: str  # Co AI proponuje
    reason: str  # Dlaczego ta zmiana
    status: Literal["pending", "accepted", "rejected", "modified"] = "pending"
    final_value: Optional[str] = None  # Co user ostatecznie wpisał (jeśli zmodyfikował)

class JobApplication(BaseModel):
    job_id: str
    user_id: str
    job_requirements: JobRequirements
    suggestions: List[Suggestion]
    status: Literal["pending", "ready", "modified", "downloaded"]
    analysis_model: Literal["quick", "full"] = "full"
    # created_at: datetime
