from fastapi import FastAPI
from app.models import Base, engine

from fastapi.middleware.cors import CORSMiddleware

from app.routers.candidates import router as candidate_router
from app.routers import auth

app = FastAPI()

#Base.metadata.create_all(bind=engine) #If in case the tables dont exist create them
#creates a recruitment.db written in models.py

app.include_router(candidate_router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


