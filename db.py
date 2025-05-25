import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 환경 변수 로드
load_dotenv()

# DB URL 설정 (환경변수 또는 기본 sqlite 파일)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./searches.db")

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 모델 임포트: Base.metadata에 테이블 메타데이터 등록을 위해 필요
# models/user.py, models/paper.py 등에 정의된 클래스가 여기에 포함됩니다
import models.user  # noqa
import models.paper  # noqa

# 애플리케이션 시작 시 자동으로 테이블 생성
Base.metadata.create_all(bind=engine)

def get_db():
    """
    FastAPI 의존성: 요청마다 DB 세션을 열고 닫아줍니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
