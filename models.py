from sqlalchemy import Column, String, DateTime, LargeBinary
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    email = Column(String(320), unique=True, nullable=False)
    phone = Column(String(32))
    gender = Column(String(16))
    password_hash = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.sysutcdatetime())

class Post(Base):
    __tablename__ = "posts"
    id = Column(UNIQUEIDENTIFIER, primary_key=True)
    user_id = Column(UNIQUEIDENTIFIER, nullable=False)
    blob_url = Column(String(2048), nullable=False)
    caption = Column(String(1024))
    created_at = Column(DateTime(timezone=True), server_default=func.sysutcdatetime())
