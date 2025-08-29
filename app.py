import os, uuid, jwt
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Post
from .auth import router as auth_router
from .storage import generate_upload_sas

app = FastAPI(title="Social API")
app.include_router(auth_router)
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")

class CreatePostReq(BaseModel):
    caption: str
    filename: str

class CreatePostResp(BaseModel):
    upload_url: str
    blob_url: str

class CommitPostReq(BaseModel):
    blob_url: str
    caption: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(authorization: str = Header(...)) -> str:
    try:
        scheme, token = authorization.split()
        assert scheme.lower() == "bearer"
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/posts/create", response_model=CreatePostResp)
def create_post(req: CreatePostReq, user_id: str = Depends(get_current_user_id)):
    blob_name = f"{user_id}/{uuid.uuid4()}-{req.filename}"
    upload_url = generate_upload_sas(blob_name)
    blob_url = upload_url.split("?")[0]
    return CreatePostResp(upload_url=upload_url, blob_url=blob_url)

@app.post("/posts/commit")
def commit_post(req: CommitPostReq, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    post = Post(user_id=user_id, blob_url=req.blob_url, caption=req.caption)
    db.add(post)
    db.commit()
    return {"status": "ok"}
