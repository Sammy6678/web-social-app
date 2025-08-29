from sqlalchemy import select
from models import User, Post
import bcrypt

def create_user(db, username, email, password, gender=None):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    u = User(username=username, email=email, password_hash=pw_hash, gender=gender)
    db.add(u); db.commit(); db.refresh(u)
    return u

def get_user_by_username(db, username):
    return db.query(User).filter(User.username==username).first()

def verify_user(db, username, password):
    u = get_user_by_username(db, username)
    if not u: return None
    if bcrypt.checkpw(password.encode(), u.password_hash.encode()):
        return u
    return None

def create_post(db, user_id, image_url, caption):
    p = Post(user_id=user_id, image_url=image_url, caption=caption)
    db.add(p); db.commit(); db.refresh(p)
    return p

def list_posts(db, limit=50):
    return db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()
