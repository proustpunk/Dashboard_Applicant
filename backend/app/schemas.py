from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Optional

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
    reviewer_id: str | None = None
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

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class CandidateListResponse(BaseModel):
    id: int
    name: str
    email: str
    role_applied: Optional[str]
    status: Optional[str]
    skills: Optional[list]
    created_at: datetime

    class Config:
        from_attributes = True