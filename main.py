# main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from recommend import recommend_related

# 1) 환경변수 로드 & 검증
load_dotenv()
AUTH_KEY = os.getenv("DBPIA_API_KEY")
if not AUTH_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")

# 2) FastAPI 앱 생성
app = FastAPI(title="Recosearch API")

# 3) /recommend API
@app.get("/recommend")
async def recommend(
    query: str = Query("", description="검색어 (생략 가능)"),
    pyear: str = Query("", description="발행 연도(YYYY, 생략 가능)"),
    pmonth: str = Query("", description="발행 월(MM, 생략 가능)"),
    category: str = Query("", regex="^[1-9]$", description="주제분류 코드(1~9, 생략 가능)")
):
    try:
        return JSONResponse(content=recommend_related(query, pyear, pmonth, category))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4) static 전체를 "/" 에 마운트 (html=True 로 index.html fallback)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True),
    name="static"
)
