from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.models import SessionLocal, User, UserRole
from app.schemas import UserCreate
from jose import JWTError

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer( #where to expect token
    tokenUrl="/auth/login"
)




pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode( 
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub") #which user this token belongs to

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    db.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

def hash_password(password: str):
    return pwd_context.hash(password) #bcrypt hash


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password)


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


@router.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=UserRole.REVIEWER
    )

    db.add(new_user)
    db.commit()

    db.close()

    return {
        "message": "User created successfully"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role.value
        }
    )

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }