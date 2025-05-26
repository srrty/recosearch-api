# schemas/recommend.py
from pydantic import BaseModel
from typing import List

class Author(BaseModel):
    name: str

class Publication(BaseModel):
    name: str
    url: str

class Recommendation(BaseModel):
    id: int              # ← 반드시 추가!
    title: str
    authors: List[Author]
    publication: Publication
    link_url: str

class RecommendResponse(BaseModel):
    pyymm: str
    recommendations: List[Recommendation]
    totalcount: int
