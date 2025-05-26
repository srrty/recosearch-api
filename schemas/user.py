# schemas/user.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    nickname: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    nickname: Optional[str] = None

# ✅ 주의: 아래처럼 UserOut만 쓰는 것도 가능함. 불필요하게 User라는 이름 중복 X!
