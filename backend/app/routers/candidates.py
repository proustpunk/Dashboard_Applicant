from fastapi import APIRouter, HTTPException
from app.services.candidate_service import generate_candidate_summary
from app.schemas import CandidateDetailResponse,SummaryResponse,CandidateResponse, ScoreCreate,ScoreResponse
from sqlalchemy.orm import joinedload
from app.models import SessionLocal, Candidate, Score
router = APIRouter()


@router.get("/candidates/{id}", response_model=CandidateDetailResponse)
def get_candidate(id: int):
    db = SessionLocal()

    candidate = db.query(Candidate).options(
    joinedload(Candidate.scores)
).filter(
    Candidate.id == id
).first()

    db.close()

    return candidate

@router.post("/candidates/{id}/scores", response_model=ScoreResponse)
def create_score(id: int, score_data: ScoreCreate):
    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == id
    ).first()

    if not candidate:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    score = Score(
        candidate_id=id,
        category=score_data.category,
        score=score_data.score,
        reviewer_id=score_data.reviewer_id,
        note=score_data.note
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    db.close()

    return score

@router.post("/candidates/{id}/summary", response_model=SummaryResponse)
async def generate_summary(id: int):
    db = SessionLocal()

    candidate = db.query(Candidate).filter(
        Candidate.id == id
    ).first()

    if not candidate:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    summary = await generate_candidate_summary(candidate)

    candidate.summary = summary

    db.commit()
    db.refresh(candidate)

    db.close()

    return candidate