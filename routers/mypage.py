# routers/mypage.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from models.user import User
from schemas.user import UserOut, UserPasswordChange
from services.auth import verify_password, get_password_hash
from routers.auth import read_current_user

router = APIRouter(prefix="/mypage", tags=["mypage"])

@router.patch(
    "/password",
    response_model=UserOut,
    summary="내 비밀번호 변경",
    description="현재 비밀번호 검증 후 새로운 비밀번호로 업데이트"
)
def change_password(
    data: UserPasswordChange,
    current_user: User = Depends(read_current_user),
    db: Session = Depends(get_db),
):
    # 1) 기존 비밀번호 확인
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="현재 비밀번호가 일치하지 않습니다."
        )
    # 2) 새 비밀번호 해시화 및 저장
    current_user.hashed_password = get_password_hash(data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
