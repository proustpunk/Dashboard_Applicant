from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import relationship,declarative_base, sessionmaker
from sqlalchemy import JSON,Column, Integer, String, DateTime
from datetime import datetime

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

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role_applied = Column(String, index=True)
    status = Column(String, index=True)
    scores = relationship(
        "Score",
        back_populates="candidate" ##FROM CANDIDATE CLASS, candidate field
    )
    skills = Column(JSON)
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
        ForeignKey("candidates.id")
    )
    candidate = relationship(
        "Candidate",
        back_populates="scores"
    )
    category = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    reviewer_id = Column(String)
    note = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )