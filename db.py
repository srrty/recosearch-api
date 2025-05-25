from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # 또는 "postgresql://user:pass@host:port/dbname"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI 의존성 주입 함수.
    요청마다 세션을 열고, 작업이 끝나면 닫아 줍니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        