from sqlalchemy.orm import Session
from models.db import Paper
from schemas.paper import PaperCreate, PaperOut

def create_paper(db: Session, paper: PaperCreate) -> PaperOut:
    db_paper = Paper(
        title=paper.title,
        authors=",".join(paper.authors),
        journal=paper.journal,
        pub_date=paper.pub_date,
        link_url=paper.link_url
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return PaperOut.from_orm(db_paper)

def list_papers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Paper).offset(skip).limit(limit).all()
