from app.models import SessionLocal, UserRole,Candidate,User
from app.routers.auth import hash_password

db = SessionLocal()


user = User(
    email="admin@test.com",
    hashed_password=hash_password("password"),
    role=UserRole.ADMIN
)

db.add(user)
db.commit()
print("Candidates created")