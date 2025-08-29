import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

server = os.getenv("SQL_SERVER")  # e.g. sql-socialapp-dev.database.windows.net
dbname = os.getenv("SQL_DB")      # socialappdb
user = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")

driver = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
conn_str = (
    f"mssql+pyodbc://{user}:{password}@{server}:1433/{dbname}?"
    f"driver={driver.replace(' ', '+')}&Encrypt=yes&TrustServerCertificate=no"
)
engine = create_engine(conn_str, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
