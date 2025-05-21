# main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from recommend import recommend_related

# 1) 환경변수 로드 & 검증
load_dotenv()
API_KEY = os.getenv("DBPIA_API_KEY")
if not API_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")

# 2) 앱 생성
app = FastAPI(title="Recosearch API")

# 3) /recommend 엔드포인트: 연도·월·주제만으로 인기 논문 추천
@app.get("/recommend")
async def recommend(
    pyear: str = Query(..., description="발행 연도(YYYY)"),
    pmonth: str = Query(..., description="발행 월(MM)"),
    category: str = Query(..., regex="^[1-9]$", description="주제분류 코드(1~9)")
):
    try:
        items = recommend_related("", pyear, pmonth, category)
        return JSONResponse(content=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4) 정적 파일 서빙 (SPA 진입점)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True),
    name="static"
)
