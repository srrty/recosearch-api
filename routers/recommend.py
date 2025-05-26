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
    pyear: int | None = Query(None, ge=1900, le=2100, description="원하는 연도(YYYY). 지정하면 pmonth와 함께 입력해야 합니다."),
    pmonth: int | None = Query(None, ge=1, le=12, description="원하는 월(MM). pyear를 지정할 경우 반드시 입력해야 합니다."),
    category: str | None = Query(None, regex="^[1-9]$", description="주제 분류 코드 (1~9)"),
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    per_page: int = Query(20, ge=1, le=100, description="페이지당 결과 수"),
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
    )
