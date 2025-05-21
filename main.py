import logging
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import xml.etree.ElementTree as ET

# --- 로깅 설정 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- API 키 로드 & 검증 ---
AUTH_KEY = os.getenv("DBPIA_API_KEY")
if not AUTH_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되지 않았습니다.")

# --- FastAPI 앱 생성 ---
app = FastAPI()

# --- 인기논문 추천 엔드포인트 ---
@app.get("/recommend")
def get_recommendations(
    pyear: int | None = Query(None, ge=1900, le=2100, description="발행 연도(YYYY). 생략 시 전월 결과"),
    pmonth: int | None = Query(None, ge=1, le=12, description="발행 월(MM). pyear 지정 시 함께 입력"),
    category: str | None = Query(None, regex="^[1-9]$", description="주제분류 코드(1~9). 생략 시 전체")
):
    if (pyear is None) ^ (pmonth is None):
        raise HTTPException(422, detail="pyear과 pmonth는 함께 지정하거나 모두 생략해야 합니다.")

    url = "http://api.dbpia.co.kr/v2/search/search.xml"
    params = {"key": AUTH_KEY, "target": "rated_art"}
    if pyear is not None:
        params["pyear"], params["pmonth"] = str(pyear), str(pmonth)
    if category:
        params["category"] = category

    resp = requests.get(url, params=params)
    logger.info(f"Request → GET {resp.url}")
    ct = resp.headers.get("Content-Type", "")
    logger.info(f"DBpia   → status={resp.status_code}, CT={ct}")

    if ct.startswith("text/html"):
        logger.error("HTML 오류 페이지:\n" + resp.text[:200])
        raise HTTPException(502, detail="DBpia 서버 오류: 인증키·파라미터·경로 확인")

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as e:
        logger.exception("XML 파싱 실패")
        raise HTTPException(502, detail=f"XML 파싱 오류: {e}")

    if root.tag == "error":
        code = root.findtext(".//Code") or "Unknown"
        raise HTTPException(502, detail=f"DBpia 오류 코드: {code}")

    totalcount = int(root.findtext(".//totalcount") or 0)
    pyymm      = root.findtext(".//pyymm")

    items: list[dict] = []
    for node in root.findall(".//item"):
        # 저자 파싱
        authors = []
        ap = node.find("authors")
        if ap is not None:
            for a in ap.findall("author"):
                name = a.get("name") or a.findtext("name")
                if name:
                    authors.append({"order": a.get("order"), "url": a.get("url"), "name": name})
            if not authors and ap.text:
                for nm in ap.text.split(","):
                    nm = nm.strip()
                    if nm:
                        authors.append({"name": nm})

        # 간행물/출판물 파싱
        pubr = node.find("publisher")
        publisher = {
            "url":  (pubr.get("url") if pubr is not None else None) or (pubr.findtext("url") if pubr is not None else None),
            "name": (pubr.get("name") if pubr is not None else None) or (pubr.findtext("name") if pubr is not None else None)
        }
        publ = node.find("publication")
        publication = {
            "url":  (publ.get("url") if publ is not None else None) or (publ.findtext("url") if publ is not None else None),
            "name": (publ.get("name") if publ is not None else None) or (publ.findtext("name") if publ is not None else None)
        }

        items.append({
            "title":        node.findtext("title"),
            "authors":      authors,
            "publisher":    publisher,
            "publication":  publication,
            "issue_yymm":   node.findtext("issue_yymm"),
            "pages":        node.findtext("pages"),
            "free_yn":      node.findtext("free_yn"),
            "price":        node.findtext("price"),
            "preview_yn":   node.findtext("preview_yn"),
            "preview":      node.findtext("preview"),
            "link_url":     node.findtext("link_url"),
            "link_api":     node.findtext("link_api")
        })

    # 여기서 한 번만 반환합니다
    return {
        "totalcount":      totalcount,
        "pyymm":           pyymm,
        "recommendations": items
    }


# --- 정적 파일 서빙 (JS, CSS 등) ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- SPA 진입점 (index.html) 직접 서빙 ---
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("static/index.html")
