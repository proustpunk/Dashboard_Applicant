from fastapi import FastAPI
from app.models import Base, engine


from app.routers.candidates import router as candidate_router

app = FastAPI()

#Base.metadata.create_all(bind=engine) #If in case the tables dont exist create them
#creates a recruitment.db written in models.py

app.include_router(candidate_router)




