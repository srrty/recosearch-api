from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    name: str

class Publication(BaseModel):
    name: Optional[str] = None

class PaperCreate(BaseModel):
    title: str
    authors: List[Author]
    publication: Publication
    link_url: Optional[str] = None

class PaperOut(BaseModel):
    title: str
    authors: List[Author]
    publication: Publication
    link_url: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[PaperOut]
