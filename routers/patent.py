
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PatentItem(BaseModel):
    title: str
    applicant: str
    application_date: str
    link: str

class PatentResponse(BaseModel):
    recommendations: List[PatentItem]

@router.get("", response_model=PatentResponse)
def search_patents(
    query: Optional[str] = None,
    pyear: Optional[int] = Query(None, ge=1900, le=2100),
    pmonth: Optional[int] = Query(None, ge=1, le=12),
    patent_no: Optional[str] = None
):
    # 테스트용 mock 데이터
    base = {
        "title": "AI 기반 영상 분석 특허",
        "applicant": "한국전자통신연구원",
        "application_date": "2023-10-20",
        "link": "https://kipris.or.kr/view?id=123456"
    }

    results = []

    if patent_no:
        results = [{
            "title": f"특허번호 {patent_no}에 대한 검색 결과",
            **base
        }]
    elif query:
        results = [{
            "title": f"'{query}' 관련 특허 검색 결과",
            **base
        }]
    elif pyear and pmonth:
        results = [{
            "title": f"{pyear}년 {pmonth}월 출원된 특허",
            **base
        }]
    else:
        raise HTTPException(status_code=400, detail="검색 조건을 최소 하나 이상 입력해야 합니다.")

    return {"recommendations": results}
