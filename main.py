# main.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import requests

# ──────────────────────────────────────────────────────────
# 1) .env 파일(로컬) 또는 Railway 환경변수에서 키 로드
load_dotenv()
API_KEY = os.getenv("DBPIA_API_KEY")
if not API_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")
# ──────────────────────────────────────────────────────────

# 2) 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3) FastAPI 앱 생성
app = FastAPI(title="Recosearch API")

# ──────────────────────────────────────────────────────────
# 4) /recommend 엔드포인트: DBpia 검색 API(v2 JSON) 호출
@app.get("/recommend")
async def recommend(
    query: str = Query(..., description="검색어 (필수)"),
    pyear: str = Query("", description="발행 연도(YYYY, 생략 가능)"),
    pmonth: str = Query("", description="발행 월(MM, 생략 가능)"),
    category: str = Query("", regex="^[1-9]$", description="주제분류 코드(1~9, 생략 가능)")
):
    # 4-1) 필수값 검증
    if not query.strip():
        raise HTTPException(status_code=400, detail="query 파라미터를 입력하세요.")

    # 4-2) DBpia 검색 API 호출
    url = "http://api.dbpia.co.kr/v2/search/search.json"
    params = {
        "key":       API_KEY,
        "target":    "se",
        "searchall": query,
        "currpage":  1,
        "rows":      10,
    }
    # optional 파라미터 추가
    if pyear and pmonth:
        params["pyear"], params["pmonth"] = pyear, pmonth
    if category:
        params["subject_cd"] = category

    resp = requests.get(url, params=params)
    logger.info(f"DBpia 검색 호출: {resp.url} → {resp.status_code}")

    # 4-3) HTML 에러 페이지 검사
    ct = resp.headers.get("Content-Type", "")
    if ct.startswith("text/html"):
        logger.error("DBpia가 HTML 오류 페이지를 반환했습니다.")
        raise HTTPException(status_code=502, detail="DBpia 검색 API 오류 (HTML 응답)")

    # 4-4) JSON 파싱
    try:
        data = resp.json()
    except ValueError:
        logger.exception("DBpia JSON 디코딩 실패")
        raise HTTPException(status_code=502, detail="DBpia JSON 파싱 오류")

    # 4-5) 결과 아이템 추출
    # JSON 구조: data.get("item") 또는 data["result"]["item"]
    items = data.get("item") or data.get("result", {}).get("item") or []
    results = []
    for it in items:
        if not isinstance(it, dict):
            continue
        results.append({
            "title":   it.get("title") or it.get("ARTICLETITLE"),
            "authors": it.get("author") or it.get("authors"),
            "link":    it.get("link") or it.get("article_link"),
        })

    return JSONResponse(content=results)
# ──────────────────────────────────────────────────────────

# 5) 정적 파일 서빙 (SPA 진입점 + CSS/JS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True),
    name="static"
)
