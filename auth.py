import os, uuid, bcrypt, jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import User
from .queue_client import enqueue_welcome

router = APIRouter(prefix="/auth", tags=["auth"])
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "60"))

class SignupReq(BaseModel):
    first_name: str
    last_name: str | None = None
    email: EmailStr
    phone: str | None = None
    gender: str | None = None
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=TokenResp)
def signup(body: SignupReq, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    uid = str(uuid.uuid4())
    pwd_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt())

    user = User(
        id=uid,
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email.lower(),
        phone=body.phone,
        gender=body.gender,
        password_hash=pwd_hash,
    )
    db.add(user)
    db.commit()

    enqueue_welcome({"email": body.email, "first_name": body.first_name})

    token = jwt.encode({
        "sub": uid,
        "email": body.email,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXP_MIN)
    }, JWT_SECRET, algorithm="HS256")
    return TokenResp(access_token=token)
