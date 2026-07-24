from app.models import SessionLocal, UserRole,Candidate,User
from app.routers.auth import hash_password

db = SessionLocal()


# user = User(
#     email="reviewer1@test.com",
#     hashed_password=hash_password("password"),
#     role=UserRole.REVIEWER
# )

user = User(
    email="reviewer2@test.com",
    hashed_password=hash_password("password"),
    role=UserRole.REVIEWER
)
db.add(user)
db.commit()
db.close()