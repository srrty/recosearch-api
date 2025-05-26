from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from schemas.user import UserOut, UserUpdate, UserPasswordChange, UserInDB
from services.auth import update_profile, delete_user, change_password
from routers.auth import read_current_user, get_current_user_model

router = APIRouter(prefix="/mypage", tags=["mypage"])

@router.patch("/profile", response_model=UserOut)
def change_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current: UserInDB = Depends(read_current_user),
) -> UserOut:
    user = update_profile(db, current, data)
    return user

@router.patch("/password", response_model=UserOut)
def change_pw(
    passwords: UserPasswordChange,
    db: Session = Depends(get_db),
    current: UserInDB = Depends(get_current_user_model),  # 여기!
) -> UserOut:
    user = change_password(db, current, passwords)
    return user

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def withdraw(
    hard: bool = False,
    db: Session = Depends(get_db),
    current: UserInDB = Depends(read_current_user)
):
    delete_user(db, current, hard)
    return
