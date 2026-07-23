from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import relationship,declarative_base, sessionmaker
from sqlalchemy import JSON,Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy import CheckConstraint


from enum import Enum
from sqlalchemy import Enum as SQLEnum

DATABASE_URL = "sqlite:///./recruitment.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class CandidateStatus(str, Enum):
    NEW = "new"
    REVIEWED = "reviewed"
    HIRED = "hired"
    REJECTED = "rejected"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role_applied = Column(String, index=True)
    status = Column(
    SQLEnum(
        CandidateStatus,
        values_callable=lambda enum: [
            item.value for item in enum
        ]
    ),
    index=True,
    default=CandidateStatus.NEW
)
    scores = relationship(
        "Score",
        back_populates="candidate", ##FROM CANDIDATE CLASS, candidate field
        cascade="all, delete-orphan"
    )
    skills = Column(JSON) #For Sqlite JSON is correct choice
    internal_notes = Column(String)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Candidate(id={self.id}, name='{self.name}')>"

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
    Integer,
    ForeignKey("candidates.id"),
    index=True
)
    candidate = relationship(
        "Candidate",
        back_populates="scores"
    )
    category = Column(String, nullable=False)
    score = Column(Integer, nullable=False) #1-5 enforced in schema
    __table_args__ = (
        CheckConstraint(
            "score >= 1 AND score <= 5",
            name="score_range_check"
        ),
    )
    reviewer_id = Column(String)
    note = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class UserRole(str, Enum):
    REVIEWER = "reviewer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.REVIEWER
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )