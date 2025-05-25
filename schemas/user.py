# schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

# 비밀번호 변경을 위한 입력 모델
class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "old_password": "기존비밀번호123",
                "new_password": "새로운비밀번호456"
            }
        }