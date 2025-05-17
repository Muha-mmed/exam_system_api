from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

import os

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False},echo=True)

localSession = sessionmaker(autoflush=False,autocommit=False,bind= engine)

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()