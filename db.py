# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# 모든 모델 import (순서는 중요 X, 단 import는 반드시 필요)
import models.user
import models.bookmark
# import models.paper 등 필요한 것들

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# (개발 중이라면) 기존 테이블 삭제
Base.metadata.drop_all(bind=engine)
# 테이블 생성
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
