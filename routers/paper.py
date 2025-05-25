from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.paper import PaperCreate, PaperOut
from services.db_service import create_paper, list_papers
from db import get_db

router = APIRouter()

@router.post("", response_model=PaperOut)
def api_create_paper(
    paper: PaperCreate,
    db: Session = Depends(get_db)
):
    return create_paper(db, paper)

@router.get("", response_model=list[PaperOut])
def api_list_papers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return list_papers(db, skip, limit)
