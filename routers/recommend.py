from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from services.dbpia import fetch_recommendations
from schemas.paper import RecommendationResponse

router = APIRouter()

@router.get("/recommend", response_model=RecommendationResponse)
def recommend(
    pyear: str | None = Query(None),
    pmonth: str | None = Query(None),
    category: int | None = Query(None),
    db: Session = Depends(get_db)
):
    # 빈 문자열과 None을 구분하지 않도록 처리
    year_val = int(pyear) if pyear and pyear.strip() else None
    month_val = int(pmonth) if pmonth and pmonth.strip() else None

    print(f"[DEBUG] /recommend called with pyear={year_val}, pmonth={month_val}, category={category}")

    # pyear, pmonth 동시 지정 또는 생략
    if (year_val is None) ^ (month_val is None):
        raise HTTPException(status_code=422, detail="pyear과 pmonth는 함께 지정하거나 모두 생략해야 합니다.")

    try:
        recs = fetch_recommendations(year_val, month_val, category)
        return {"recommendations": recs}
    except Exception as e:
        print(f"[ERROR] exception in recommend: {e}")
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")
