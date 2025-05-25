# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from db import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from services.auth import (
    register_user,
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    회원가입:
    - 중복된 아이디면 400, "중복된 아이디입니다!" 반환
    - 성공 시 생성된 User 객체(JSON) 반환
    """
    try:
        user = register_user(db, user_in.username, user_in.password)
    except ValueError as e:
        # 서비스 레이어에서 던진 "중복된 아이디입니다!" 를 그대로 돌려줌
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    로그인:
    - 존재하지 않는 아이디면 400, "존재하지 않는 아이디입니다!" 반환
    - 비밀번호 불일치면 400, "비밀번호를 다시 확인해 주세요!" 반환
    - 성공 시 토큰을 {"access_token":..., "token_type":"bearer"} 반환
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except LookupError as e:
        # 서비스 레이어에서 던진 "존재하지 않는 아이디입니다!" 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        # 서비스 레이어에서 던진 "비밀번호를 다시 확인해 주세요!"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    토큰에서 사용자명(sub) 꺼내서 DB 조회 후 User 반환
    검증 실패 시 401 에러
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효한 자격증명이 아닙니다."
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise credentials_exception
    return user
