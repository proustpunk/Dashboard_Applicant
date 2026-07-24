from app.models import SessionLocal, UserRole, User
from app.routers.auth import hash_password

db = SessionLocal()

existing = db.query(User).filter(User.email == "admin@test.com").first()

if not existing:
    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("adminpassword"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print("Admin created.")
else:
    print("Admin already exists, skipping.")

db.close()