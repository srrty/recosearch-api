# main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests

load_dotenv()
AUTH_KEY = os.getenv("DBPIA_API_KEY")
if not AUTH_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")

app = FastAPI()

@app.get("/recommend")
async def recommend(
    query: str = Query(..., description="검색어 (필수)")
):
    # 1) 파라미터 검증
    if not query.strip():
        raise HTTPException(status_code=400, detail="query 파라미터를 입력하세요.")

    # 2) 검색용 엔드포인트로 변경
    url = "http://api.dbpia.co.kr/v2/search/search.json"
    params = {
        "key": AUTH_KEY,
        "target": "se",
        "searchall": query,
        "currpage": 1,
        "rows": 10,
    }
    resp = requests.get(url, params=params)
    if resp.headers.get("Content-Type", "").startswith("text/html"):
        # HTML 에러 페이지가 왔다는 뜻
        raise HTTPException(status_code=502, detail="DBpia 검색 API 오류")

    # 3) JSON 파싱
    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="DBpia JSON 디코딩 실패")

    # 4) 실제 결과 아이템 추출 (API 구조에 맞게)
    items = data.get("item") or data.get("result", {}).get("item") or []
    results = []
    for it in items:
        results.append({
            "title": it.get("title") or it.get("ARTICLETITLE"),
            "authors": it.get("author") or it.get("authors"),
            "link": it.get("link") or it.get("article_link"),
        })
    return JSONResponse(content=results)
