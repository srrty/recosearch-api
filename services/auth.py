# services/auth.py

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session

from models.user import User

# ── 기존 JWT · password 헬퍼 ──
SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ── 여기에 추가 ──

def register_user(db: Session, username: str, password: str) -> User:
    """
    새 사용자를 DB에 등록합니다.
    이미 같은 username이 있으면 ValueError를 던집니다.
    """
    existing = db.query(User).filter_by(username=username).first()
    if existing:
        raise ValueError("중복된 아이디입니다!")
    hashed_pw = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    사용자명·비밀번호로 인증합니다.
    사용자명 미존재 시 LookupError,
    비밀번호 불일치 시 PermissionError를 던집니다.
    """
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise LookupError("존재하지 않는 아이디입니다!")
    if not verify_password(password, user.hashed_password):
        raise PermissionError("비밀번호를 다시 확인해 주세요!")
    return user
