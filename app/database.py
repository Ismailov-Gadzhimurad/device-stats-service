from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.services.config import settings
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=10,
    pool_recycle=3600,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(engine, retries=10, delay=3):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Database connected!")
                return
        except OperationalError as e:
            print(f"Waiting for database... ({i+1}/{retries})")
            time.sleep(delay)
    raise Exception("Could not connect to database after multiple attempts")
