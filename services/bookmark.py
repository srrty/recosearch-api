# services/bookmark.py

from sqlalchemy.orm import Session
from models.user import User as UserModel
from models.bookmark import Bookmark

def add_bookmark(
    db: Session,
    user: UserModel,
    paper_id: int,
    paper_title: str,
    paper_link:  str  
) -> Bookmark:
    """
    paper_id, paper_title 을 함께 받아
    북마크 레코드를 생성 후 반환합니다.
    """
    bm = Bookmark(
        user_id=user.id,
        paper_id=paper_id,
        paper_title=paper_title,
        paper_link= paper_link
    )
    db.add(bm)
    db.commit()
    db.refresh(bm)
    return bm

def list_bookmarks(db: Session, user: UserModel) -> list[Bookmark]:
    """
    DB에서 현재 유저의 Bookmark ORM 객체 리스트를 그대로 반환합니다.
    Pydantic BookmarkOut(orm_mode=True) 이 paper_title 등도 직렬화해 줍니다.
    """
    return db.query(Bookmark).filter_by(user_id=user.id).all()

def remove_bookmark(
    db: Session,
    user: UserModel,
    bm_id: int
) -> None:
    """
    bookmark_id 가 user 의 것인지 확인 후 삭제합니다.
    """
    bm = db.query(Bookmark).filter_by(id=bm_id, user_id=user.id).first()
    if bm:
        db.delete(bm)
        db.commit()
