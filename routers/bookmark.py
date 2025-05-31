# routers/bookmark.py

from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session

from db import get_db
from models.user import User as UserModel
from services.bookmark import add_bookmark, list_bookmarks, remove_bookmark
from schemas.bookmark import BookmarkCreate, BookmarkOut
from routers.auth import read_current_user

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmarks"],
)


@router.get("/", response_model=list[BookmarkOut])
def get_my_bookmarks(
    db: Session = Depends(get_db),
    current: UserModel = Depends(read_current_user),
):
    """
    현재 로그인한 사용자의 모든 북마크를 반환합니다.
    """
    return list_bookmarks(db, current)


@router.post(
    "/",
    response_model=BookmarkOut,
    status_code=status.HTTP_201_CREATED,
)
def create_bookmark(
    data: BookmarkCreate = Body(...),           # paper_id, paper_title, paper_link
    db: Session = Depends(get_db),
    current: UserModel = Depends(read_current_user),
):
    """
    즐겨찾기 생성: 받은 paper_id, paper_title, paper_link 를 저장하고,
    생성된 Bookmark ORM 객체를 그대로 반환합니다.
    """
    bm = add_bookmark(
        db,
        current,
        data.paper_id,
        data.paper_title,
        data.paper_link,
    )
    return bm


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current: UserModel = Depends(read_current_user),
):
    """
    즐겨찾기 삭제: bookmark_id가 현재 유저 소유인지 확인 후 삭제합니다.
    """
    remove_bookmark(db, current, bookmark_id)
    return
