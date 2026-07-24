from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class CandidateCreate(BaseModel):
    name: str
    email: str
    role_applied: str
    skills: list[str] | None = None

class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    role_applied: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }



class ScoreCreate(BaseModel):
    category: str
    score: int = Field(ge=1, le=5)
    note: str | None = None

class ScoreResponse(BaseModel):
    id: int
    candidate_id: int
    category: str
    score: int
    reviewer_id: str | None
    note: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class SummaryResponse(BaseModel):
    id: int
    summary: str

    model_config = {
        "from_attributes": True
    }


class CandidateDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    role_applied: str
    status: str
    skills: list[str] | None
    summary: str | None
    scores: list[ScoreResponse] = []
    internal_notes: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class InternalNoteUpdate(BaseModel):

    internal_notes: str

class CandidateAdminDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    role_applied: str
    status: str
    skills: list[str] | None
    summary: str | None
    internal_notes: str | None
    scores: list[ScoreResponse] = []

    created_at: datetime

    model_config = {
        "from_attributes": True
    }
class CandidateListResponse(BaseModel): #Score is a long list so is the summary. They are avoided here
    id: int
    name: str
    email: str
    role_applied: Optional[str]
    status: Optional[str]
    skills: Optional[list]
    created_at: datetime

    class Config:
        from_attributes = True