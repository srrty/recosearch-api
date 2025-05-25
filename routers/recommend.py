from fastapi import APIRouter, Query, HTTPException
from services.dbpia import fetch_recommendations
from models.paper import RecommendationResponse

router = APIRouter()

@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    pyear: int | None = Query(None, ge=1900, le=2100),
    pmonth: int | None = Query(None, ge=1, le=12),
    category: str | None = Query(None, regex="^[1-9]$")
):
    # pyear과 pmonth는 함께 입력하거나 모두 생략해야 함을 검사
    if (pyear is None) ^ (pmonth is None):
        raise HTTPException(422, detail="pyear과 pmonth는 함께 지정하거나 모두 생략해야 합니다.")
    # 서비스 레이어로 로직 위임
    return fetch_recommendations(pyear, pmonth, category)