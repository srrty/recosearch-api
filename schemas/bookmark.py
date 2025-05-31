#schemas/bookmark.py
from pydantic import BaseModel
from datetime import datetime

class BookmarkCreate(BaseModel):
    paper_id: int
    paper_title: str
    paper_link:  str  

class BookmarkOut(BaseModel):
    id: int
    paper_id: int
    paper_title: str
    paper_link:  str  
    created_at: datetime

    class Config:
        orm_mode = True