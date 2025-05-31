# routers/recommend.py
from fastapi import APIRouter, Query, HTTPException
from services.dbpia import fetch_recommendations
from models.paper import RecommendationResponse

router = APIRouter(
     prefix="/recommend",
     tags=["recommend"]
 )
 
@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    pyear: int | None = Query(None, ge=1900, le=2100),
    pmonth: int | None = Query(None, ge=1, le=12),
    category: str | None = Query(None, regex="^[1-9]$"), 
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity", regex="^(popularity|title)$"),  # date → title
    order: str = Query("desc", regex="^(asc|desc)$"),  # 👈 추가
    query: str | None = Query(None, max_length=100),  # 👈 추가
):
    # pyear과 pmonth는 함께 입력하거나 모두 생략해야 함을 검사
    if (pyear is None) ^ (pmonth is None):
        raise HTTPException(422, detail="pyear과 pmonth는 함께 지정하거나 모두 생략해야 합니다.")
    # str로 변환하여 서비스 호출
    py = str(pyear) if pyear is not None else ""
    pm = str(pmonth) if pmonth is not None else ""
    return fetch_recommendations(
        pyear=py,
        pmonth=pm,
        category=category or "",
        page=page,
        per_page=per_page,
        sort_by=sort_by, # 👈 추가
        order=order, # 👈 추가
        title=query or "",  # 👈 추가
    )