from fastapi import APIRouter, HTTPException
from app.services.candidate_service import generate_candidate_summary
from app.schemas import CandidateAdminDetailResponse,CandidateDetailResponse,SummaryResponse,CandidateResponse, ScoreCreate,ScoreResponse
from sqlalchemy.orm import joinedload
from fastapi.responses import StreamingResponse
import json
from typing import Optional
from sqlalchemy import or_
from fastapi import Query
from app.schemas import CandidateListResponse
from app.services.event_manager import event_manager
from app.services.event_manager import event_manager
from app.models import SessionLocal, Candidate, Score
from fastapi import Depends
from app.routers.auth import get_current_user
from app.models import User, UserRole
router = APIRouter()


@router.get("/candidates/{id}")
def get_candidate(id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    candidate = db.query(Candidate).options(
    joinedload(Candidate.scores)
).filter(
    Candidate.id == id
).first()

    if not candidate:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Candidate not Found"
        )

    if current_user.role == UserRole.REVIEWER:
        candidate.scores = [
            score for score in candidate.scores
            if score.reviewer_id == current_user.email
        ]

    db.close()

    return CandidateAdminDetailResponse.model_validate(
        candidate
    )

@router.post("/candidates/{id}/scores", response_model=ScoreResponse)
async def create_score(id: int, score_data: ScoreCreate, current_user: User = Depends(get_current_user)): #PUBLISH IS ASYNC
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
        reviewer_id=current_user.email,
        note=score_data.note
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    await event_manager.publish(
    id,
    {
        "candidate_id": id,
        "category": score.category,
        "score": score.score,
        "reviewer_id": score.reviewer_id,
        "note": score.note,
    },
)

    db.close()

    return score

@router.post("/candidates/{id}/summary", response_model=SummaryResponse)
async def generate_summary(id: int, current_user: User = Depends(get_current_user)):
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


@router.get("/candidates/{id}/stream")
async def stream_scores(id: int):

    queue = await event_manager.subscribe(id)

    async def event_generator():

        try:
            while True:
                message = await queue.get()

                yield f"data: {json.dumps(message)}\n\n"

        finally:
            await event_manager.unsubscribe(id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.get("/candidates", response_model=list[CandidateListResponse])
def get_candidates(
    status: Optional[str] = None,
    role_applied: Optional[str] = None,
    skill: Optional[str] = None,
    keyword: Optional[str] = None,
    offset: int = 0,
    limit: int = Query(default=20, le=50)
):
    db = SessionLocal()

    query = db.query(Candidate)

    # status filter
    if status:
        query = query.filter(
            Candidate.status == status
        )

    # role filter
    if role_applied:
        query = query.filter(
            Candidate.role_applied == role_applied
        )

    # skill filter
    if skill:
        query = query.filter(
            Candidate.skills.contains([skill])
        )

    # keyword search
    if keyword:
        search = f"%{keyword}%"

        query = query.filter(
            or_(
                Candidate.name.ilike(search),
                Candidate.email.ilike(search),
                Candidate.role_applied.ilike(search)
            )
        )

    candidates = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    db.close()

    return candidates