# main.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from recommend import recommend_related

# 1) .env 파일에서 DBPIA_API_KEY 로드 및 검증
load_dotenv()
AUTH_KEY = os.getenv("DBPIA_API_KEY")
if not AUTH_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")

# 2) 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3) FastAPI 앱 생성
app = FastAPI(title="Recosearch API")

# 4) /recommend 엔드포인트: 모든 파라미터를 Optional로 처리
@app.get("/recommend")
async def recommend(
    query: str | None = Query(None, description="검색어 (선택)"),
    pyear: str | None = Query(None, description="발행 연도(YYYY, 선택)"),
    pmonth: str | None = Query(None, description="발행 월(MM, 선택)"),
    category: str | None = Query(None, regex="^[1-9]$", description="주제분류 코드(1~9, 선택)")
):
    # None 값을 빈 문자열로 변환
    q = query or ""
    y = pyear or ""
    m = pmonth or ""
    c = category or ""
    try:
        results = recommend_related(q, y, m, c)
        return JSONResponse(content=results)
    except Exception:
        logger.exception("Error while handling /recommend")
        raise HTTPException(status_code=500, detail="서버 내부 에러가 발생했습니다.")

# 5) 정적 파일 서빙 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# /static/* 경로에서 CSS/JS 등 정적 자원 제공
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# / 요청은 static/index.html 반환 (SPA 진입점)
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))
