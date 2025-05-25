from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.paper import Paper as PaperModel
from schemas.paper import PaperCreate, PaperOut

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/", response_model=PaperOut)
def create_paper(
    paper_in: PaperCreate,
    db: Session = Depends(get_db)
):
    """새 논문을 생성하고 반환합니다."""
    paper = PaperModel(
        title=paper_in.title,
        authors=','.join([author.name for author in paper_in.authors]),
        journal=paper_in.publication.name or "",
        url=paper_in.link_url or ""
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)
    return PaperOut(
        title=paper.title,
        authors=[{"name": name} for name in paper.authors.split(',') if name],
        publication={"name": paper.journal},
        link_url=paper.url
    )

@router.get("/", response_model=list[PaperOut])
def list_papers(db: Session = Depends(get_db)):
    """저장된 모든 논문 목록을 반환합니다."""
    papers = db.query(PaperModel).all()
    return [
        PaperOut(
            title=p.title,
            authors=[{"name": name} for name in p.authors.split(',') if name],
            publication={"name": p.journal},
            link_url=p.url
        ) for p in papers
    ]
