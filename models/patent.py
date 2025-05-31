from pydantic import BaseModel
from typing import List

class PatentItem(BaseModel):
    title: str
    applicant: str
    application_date: str
    link: str

class PatentResponse(BaseModel):
    patents: List[PatentItem]
