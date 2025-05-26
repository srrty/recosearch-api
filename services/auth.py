# services/auth.py
import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user import User as UserModel
from schemas.user import UserCreate, UserInDB, UserUpdate, UserPasswordChange, UserOut

# 환경 변수로부터 비밀키와 알고리즘 로드
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def register_user(db: Session, user_create: UserCreate) -> UserModel:
    hashed_password = get_password_hash(user_create.password)
    user = UserModel(
        username=user_create.username,
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserInDB]:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return UserInDB.from_orm(user)


def update_profile(db: Session, user: UserModel, data: UserUpdate) -> UserModel:
    if data.username:
        user.username = data.username
    if data.nickname is not None:
        user.nickname = data.nickname
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: UserModel, hard: bool = False):
    if hard:
        db.delete(user)
    else:
        user.is_active = False
    db.commit()

def change_password(db: Session, user: UserInDB, passwords: UserPasswordChange) -> UserOut:
    # 1. 현재 비밀번호 검증
    if not verify_password(passwords.current_password, user.hashed_password):
        raise ValueError("현재 비밀번호가 일치하지 않습니다.")
    # 2. 새 비밀번호로 변경
    hashed = get_password_hash(passwords.new_password)
    db_user = db.query(UserModel).filter(UserModel.id == user.id).first()
    db_user.hashed_password = hashed
    db.commit()
    db.refresh(db_user)
    return UserOut.from_orm(db_user)


