import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
import crud
from azure.storage.blob import BlobServiceClient
import uuid, requests

# Ensure tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Langunana Backend")

# CORS - allow frontend host(s)
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', '*')
app.add_middleware(CORSMiddleware, allow_origins=[FRONTEND_ORIGIN] if FRONTEND_ORIGIN!='*' else ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BLOB_CONN = os.getenv('BLOB_CONN')
BLOB_CONTAINER = os.getenv('BLOB_CONTAINER', 'images')
WELCOME_FUNC_URL = os.getenv('WELCOME_FUNC_URL')

blob_client = None
if BLOB_CONN:
    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)
    blob_client = blob_service.get_container_client(BLOB_CONTAINER)
    try:
        blob_client.get_container_properties()
    except Exception:
        blob_client.create_container()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/signup')
async def signup(email: str = Form(...), username: str = Form(...), password: str = Form(...), gender: str = Form(None)):
    db = next(get_db())
    exists = crud.get_user_by_username(db, username)
    if exists:
        raise HTTPException(status_code=400, detail="username already exists")
    user = crud.create_user(db, username=username, email=email, password=password, gender=gender)
    # trigger welcome func
    if WELCOME_FUNC_URL:
        try:
            requests.post(WELCOME_FUNC_URL, json={'email': email, 'username': username, 'type': 'signup'}, timeout=5)
        except Exception as e:
            print("welcome email trigger failed", e)
    return {'status':'ok', 'user_id': user.id}

@app.post('/signin')
async def signin(username: str = Form(...), password: str = Form(...)):
    db = next(get_db())
    user = crud.verify_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    # optional login email
    if WELCOME_FUNC_URL:
        try:
            requests.post(WELCOME_FUNC_URL, json={'email': user.email, 'username': username, 'type': 'login'}, timeout=5)
        except:
            pass
    return {'status':'ok', 'user_id': user.id}

@app.post('/post')
async def post(user_id: int = Form(...), caption: str = Form(None), image: UploadFile = File(None)):
    db = next(get_db())
    image_url = None
    if image and blob_client:
        ext = image.filename.split('.')[-1]
        blob_name = f"{user_id}/{uuid.uuid4()}.{ext}"
        blob_client.upload_blob(blob_name, image.file.read(), overwrite=True)
        acct_url = blob_client.url.rsplit('/',1)[0]  # container url
        image_url = f"{acct_url}/{blob_name}"
    p = crud.create_post(db, user_id, image_url, caption)
    return {'status':'ok', 'id':p.id, 'image_url':image_url}

@app.get('/posts')
def get_posts():
    db = next(get_db())
    items = crud.list_posts(db)
    out = [{'id':i.id,'user_id':i.user_id,'image_url':i.image_url,'caption':i.caption,'created_at':i.created_at.isoformat()} for i in items]
    return out
