#models/paper.py
from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    order: Optional[int]
    url:   Optional[str]
    name:  str

class Publication(BaseModel):
    url:  Optional[str]
    name: Optional[str]

class Recommendation(BaseModel):
    id: Optional[int]
    paper_id: Optional[int]
    title:        Optional[str]
    authors:      List[Author]
    publisher:    Publication
    publication:  Publication
    issue_yymm:   Optional[str]
    pages:        Optional[str]
    free_yn:      Optional[str]
    price:        Optional[str]
    preview_yn:   Optional[str]
    preview:      Optional[str]
    link_url:     Optional[str]
    link_api:     Optional[str]

class RecommendationResponse(BaseModel):
    totalcount:      int
    pyymm:           Optional[str]
    recommendations: List[Recommendation]

    class Config:
        orm_mode = True
