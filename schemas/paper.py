from datetime import date
from pydantic import BaseModel

class PaperBase(BaseModel):
    title: str
    authors: list[str]
    journal: str | None = None
    pub_date: date | None = None
    link_url: str | None = None

class PaperCreate(PaperBase):
    pass

class PaperOut(PaperBase):
    id: int

    class Config:
        orm_mode = True
