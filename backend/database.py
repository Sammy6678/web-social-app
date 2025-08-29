from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

DB_CONN = os.getenv('DB_CONN')
if not DB_CONN:
    raise Exception('DB_CONN not set')

engine = create_engine(DB_CONN, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
